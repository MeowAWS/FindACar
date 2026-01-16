from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
DATABASE_NAME = ("Toyota_cars")
COLLECTION_NAME = ("listings")

def create_damage_labels_numerical(document):
    """
    Create damage_labels_numerical property that counts 1s in each damage_labels array.
    Also adds total_images count from exterior_images.
    """
    if 'damage_labels' not in document:
        return None
    
    damage_labels = document['damage_labels']
    damage_labels_numerical = {}
    
    # Process each damage type
    for damage_type, values in damage_labels.items():
        # Count the number of 1s in the array
        count_of_ones = values.count(1)
        damage_labels_numerical[damage_type] = count_of_ones
    
    # Get total_images from exterior_images array
    total_images = 0
    if 'exterior_images' in document and document['exterior_images'] is not None:
        total_images = len(document['exterior_images'])
    
    # Add total_images to the result
    damage_labels_numerical['total_images'] = total_images
    
    return damage_labels_numerical

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
        # Generate damage_labels_numerical
        damage_labels_numerical = create_damage_labels_numerical(doc)
        
        if damage_labels_numerical is not None:
            # Update the document with the new field
            collection.update_one(
                {"_id": doc["_id"]},
                {"$set": {"damage_labels_numerical": damage_labels_numerical}}
            )
            updated_count += 1
            print(f"Updated document with _id: {doc['_id']}")
            print(f"  Numerical counts: {damage_labels_numerical}")
            print(f"    Objects done: {updated_count}")
    
    print(f"\nTotal documents updated: {updated_count}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    main()