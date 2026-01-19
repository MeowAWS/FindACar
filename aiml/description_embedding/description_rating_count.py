from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
DATABASE_NAME = "Toyota_cars"
COLLECTION_NAME = "listings"

def get_description_rating(document):
    """
    Get description_rating based on which rating key is set to 1.
    Returns a number from 1 to 5, or 0 if has_description is 0.
    """
    # Check if has_description is 0
    if 'has_description' in document and document['has_description'] == 0:
        return 0
    
    rating_map = {
        "Excellent": 5,
        "Above Average": 4,
        "Average": 3,
        "Below Average": 2,
        "Bad": 1
    }
    
    # Check each rating key in the document
    for rating_key, rating_value in rating_map.items():
        if rating_key in document and document[rating_key] == 1:
            return rating_value
    
    # Return None if no rating is found
    return None

def main():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Find all documents that have damage_labels
    query = {"damage_labels": {"$exists": True}}
    documents = collection.find(query)
    
    updated_count = 0
    
    for doc in documents:
        # Get description rating
        description_rating = get_description_rating(doc)
        
        if description_rating is not None:
            # Update the document with the new field
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"description_rating": description_rating}}
            )
            updated_count += 1
            print(f"Updated document with _id: {doc['_id']}, Rating: {description_rating}, Objects done: {updated_count}")
        else:
            print(f"Skipped document with _id: {doc['_id']} - No rating found")
    
    print(f"\nTotal documents updated: {updated_count}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()