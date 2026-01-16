from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
DATABASE_NAME = ("Honda_cars")
COLLECTION_NAME = ("listings")

def add_data_for_ml(document):
    """
    Create data-for-ml property with 20 columns, padding with -1 where needed.
    """
    if 'damage_labels' not in document:
        return None
    
    damage_labels = document['damage_labels']
    data_for_ml = {}
    
    # Process each damage type
    for damage_type, values in damage_labels.items():
        # Get the current number of values
        current_length = len(values)
        
        # Create new list with existing values
        ml_values = values.copy()
        
        # Pad with -1 to reach 20 columns
        padding_needed = 20 - current_length
        if padding_needed > 0:
            ml_values.extend([-1] * padding_needed)
        
        # If somehow there are more than 20, truncate (shouldn't happen based on your description)
        data_for_ml[damage_type] = ml_values[:20]
    
    return data_for_ml

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
        # Generate data-for-ml
        data_for_ml = add_data_for_ml(doc)
        
        if data_for_ml is not None:
            # Update the document with the new field
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"data-for-ml": data_for_ml}}
            )
            updated_count += 1
            print(f"Updated document with _id: {doc['_id']}")
    
    print(f"\nTotal documents updated: {updated_count}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()