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
db = mdb_client["Suzuki_cars"]   ####################################################################################################

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
    # English
    "excellent condition",
    "well maintained",
    "genuine car",
    "non accidental",
    "original paint",
    "bumper to bumper genuine",
    "engine in perfect condition",
    "smooth drive",
    "just buy and drive",
    "family used car",
    "first owner",
    "low mileage",
    "documents complete",
    "original file and smart card",
    "soundless engine",
    "clean interior",
    "neat condition",

    # Pakistani English / Urdu mix
    "total genuine",
    "100% genuine",
    "scratchless",
    "no touching",
    "no work required",
    "koi kaam nahi",
    "engine 100%",
    "suspension smooth",
    "Alhamdulillah",
    "bilkul theek",
    "new condition",
    "lush condition",
    "water drop engine",
    "biometric on the spot",
    "book file complete"
]

bad_refs = [
    # English
    "accident car",
    "accident damaged",
    "engine problem",
    "gear problem",
    "suspension issue",
    "body work required",
    "paint work",
    "dent and scratch",
    "major repair needed",
    "mechanical issue",
    "poor condition",
    "rust",
    "chassis damage",

    # Pakistani phrasing
    "touching",
    "shower",
    "patch",
    "half paint",
    "1.5 piece",
    "alignment work needed",
    "engine kharab",
    "gear kharab",
    "accident hai",
    "kaam hai",
    "work required",
    "meter reversed",
    "document issue",
    "file missing"
]

def check_description(car_description, og_numeric_rating, good_vector, bad_vector):
    if not car_description or not car_description.strip():
        has_description = 0
        rating = "Null"
    else:
        rating = get_rating_of_a_car(car_description, og_numeric_rating, good_vector, bad_vector)
        has_description = 1
    return has_description, rating

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
                {"$set": {"has_description": 1,"Excellent": excellent_state,"Above Average": above_avg_state, "Average": avg_state, "Below Average": below_avg_state, "Bad": bad_state}}
            )
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1} for doc {doc_id}")
            else:
                print(f"Failed to update doc {doc_id}: {e}")

def write_null_rating_back_to_db(doc_id, collection):

    max_retries = 3
    for attempt in range(max_retries):
        try:
            collection.update_one(
                {"_id": doc_id},
                {"$set": {"has_description": 0,"Excellent": None,"Above Average": None, "Average": None, "Below Average": None, "Bad": None}}
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
            has_description, rating = check_description(description, og_numeric_rating, good_vector, bad_vector)
            if has_description:
                write_rating_back_to_db(car["_id"], rating, collection)
            else:
                write_null_rating_back_to_db(car["_id"], collection)
            print(f"Embedded {i+1}/{len(docs)}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        mdb_client.close()
        print("MongoDB connection closed")

# ---------------- RUN ----------------
description_embedder("listings")