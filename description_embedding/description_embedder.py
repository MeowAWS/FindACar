import numpy as np
from numpy.linalg import norm
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from sentence_transformers import SentenceTransformer

# Load .env
load_dotenv()
mongo_url = os.getenv("MONGO_URL")

# MongoDB client with timeout settings
mdb_client = MongoClient(
    mongo_url,
    serverSelectionTimeoutMS=5000,
    connectTimeoutMS=10000,
    socketTimeoutMS=30000,
    maxPoolSize=50,
    retryWrites=True
)
db = mdb_client["Honda_cars"]   ####################################################################################################

# Load sentence-transformers model
model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------------- HELPER FUNCTIONS ----------------
def embed(text):
    """Return embedding vector for a text."""
    return model.encode(text)

def avg(vectors):
    return np.mean(vectors, axis=0)

def cos(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

# ---------------- VARIABLES ----------------
good_refs = [
    "well maintained car with low mileage and no accidents",
    "clean car with full service history",
    "excellent condition vehicle",
    "car is in pristine condition, no dents or scratches",
    "smooth engine performance and recently serviced",
    "interior and exterior are very clean and intact",
    "all original parts and properly maintained",
    "low usage, tires and brakes in excellent condition",
    "owner is careful and car drives like new",
    "perfect running condition with no mechanical issues",
    "minor cosmetic wear only, fully functional",
    "reliable car with detailed maintenance records",
    "Gari achi condition me hai, low mileage aur koi accident nahi",
    "Saaf suthri gari, full service history ke sath",
    "Perfect condition me gari",
    "Gari bilkul nayi jaisi, koi dents ya scratches nahi",
    "Engine smooth hai, recently serviced",
    "Interior aur exterior bilkul saaf aur intact hai",
    "Saare original parts hain aur properly maintain hui hai",
    "Kam use hui, tires aur brakes perfect condition me",
    "Owner careful hai aur gari bilkul nayi jaisi chalti hai",
    "Perfect running condition, koi mechanical issues nahi",
    "Minor cosmetic wear hai, fully functional",
    "Reliable gari, maintenance records available",
    "Koi kam nahi hone wala",
    "1st owner",
    "scratchless body"
]

bad_refs = [
    "accident damaged car",
    "engine problems and rust",
    "poor condition vehicle with issues",
    "car has major dents and paint peeling",
    "frequent mechanical failures and service needed",
    "interior and exterior badly worn out",
    "brakes and suspension need replacement",
    "high mileage and poorly maintained",
    "significant engine noise and transmission issues",
    "rust on chassis and underbody",
    "owner reports multiple breakdowns",
    "unreliable car with missing parts",
    "Accident damaged gari",
    "Engine me problems aur rust hai",
    "Poor condition, kai issues hain",
    "Gari me bohot dents aur paint peeling hai",
    "Mechanical failures frequent, service required",
    "Interior aur exterior badly worn out",
    "Brakes aur suspension replace karne ki zarurat hai",
    "High mileage aur poorly maintained",
    "Engine me noise aur transmission problems",
    "Chassis aur underbody me rust hai",
    "Owner ne multiple breakdowns report kiye",
    "Unreliable gari, kuch parts missing hain",
    "Alignment work needed",
    "Small patch"
]

# ---------------- RATING FUNCTIONS ----------------
def get_rating_of_a_car(car_description, og_numeric_rating, good_vector, bad_vector):
    car_vec = embed(car_description)

    try:
        og_numeric_rating = float(og_numeric_rating)
        has_numeric_rating = True
    except (TypeError, ValueError):
        has_numeric_rating = False

    if has_numeric_rating:
        if og_numeric_rating > 8:
            rating = "Excellent"
        elif og_numeric_rating < 2:
            rating = "Bad"
        else:
            good_score = cos(car_vec, good_vector)
            bad_score = cos(car_vec, bad_vector)

            if good_score > bad_score + 0.05:
                rating = "Above Average"
            elif bad_score > good_score + 0.05:
                rating = "Average"
            else:
                rating = "Below Average"
    else:
        good_score = cos(car_vec, good_vector)
        bad_score = cos(car_vec, bad_vector)

        if good_score > bad_score + 0.05:
            rating = "Above Average"
        elif bad_score > good_score + 0.05:
            rating = "Average"
        else:
            rating = "Below Average"

    return rating

def get_car_listings(collection_name):
    collection = db[collection_name]
    return list(collection.find({}).batch_size(100))

def write_rating_back_to_db(doc_id, rating, collection):
    excellent_state = 1 if rating == "Excellent" else 0
    above_avg_state = 1 if rating == "Above Average" else 0
    avg_state = 1 if rating == "Average" else 0
    below_avg_state = 1 if rating == "Below Average" else 0
    bad_state = 1 if rating == "Bad" else 0

    max_retries = 3
    for attempt in range(max_retries):
        try:
            collection.update_one(
                {"_id": doc_id},
                {"$set": {"Excellent": excellent_state,"Above Average": above_avg_state, "Average": avg_state, "Below Average": below_avg_state, "Bad": bad_state}}
            )
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1} for doc {doc_id}")
            else:
                print(f"Failed to update doc {doc_id}: {e}")

# ---------------- MAIN FUNCTION ----------------
def description_embedder(collection_name):
    try:
        # Test connection
        mdb_client.admin.command('ping')
        print("MongoDB connection successful")
        
        docs = get_car_listings(collection_name)
        
        # Precompute Good/Bad vectors
        good_vector = np.mean(np.vstack([embed(x) for x in good_refs]), axis=0)
        bad_vector  = np.mean(np.vstack([embed(x) for x in bad_refs]), axis=0)

        
        collection = db[collection_name]
        
        for i, car in enumerate(docs):
            description = car.get("description", "")
            og_numeric_rating = car.get("rating", "")
            rating = get_rating_of_a_car(description, og_numeric_rating, good_vector, bad_vector)
            write_rating_back_to_db(car["_id"], rating, collection)
            print(f"Embedded {i+1}/{len(docs)}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mdb_client.close()
        print("MongoDB connection closed")

# ---------------- RUN ----------------
description_embedder("listings")