from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
SOURCE_DATABASE = "Toyota_cars"
SOURCE_COLLECTION = "listings"
TARGET_DATABASE = "Toyota_cars_2"  # New database name
TARGET_COLLECTION = "listings"  # Collection name in new database

def migrate_data():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    
    # Source database and collection
    source_db = client[SOURCE_DATABASE]
    source_collection = source_db[SOURCE_COLLECTION]
    
    # Target database and collection (will be created automatically)
    target_db = client[TARGET_DATABASE]
    target_collection = target_db[TARGET_COLLECTION]
    
    # Find all documents that have primary_key, sorted in ascending order
    query = {"primary_key": {"$exists": True}}
    documents = source_collection.find(query).sort("primary_key", 1)
    
    migrated_count = 0
    
    for doc in documents:
        # Create new document with only the specified fields
        new_doc = {
            "primary_key": doc.get("primary_key"),
            "URL": doc.get("URL"),
            "Title": doc.get("Title"),
            "brand": doc.get("brand"),
            "name": doc.get("name"),
            "rating": doc.get("rating"),
            "images": doc.get("images"),
            "description": doc.get("description")
        }
        
        # Insert into target collection
        target_collection.insert_one(new_doc)
        migrated_count += 1
        
        print(f"Migrated document with primary_key: {doc.get('primary_key')}, Total: {migrated_count}")
    
    print(f"\n{'='*60}")
    print(f"Migration Complete!")
    print(f"Total documents migrated: {migrated_count}")
    print(f"Source: {SOURCE_DATABASE}.{SOURCE_COLLECTION}")
    print(f"Target: {TARGET_DATABASE}.{TARGET_COLLECTION}")
    print(f"{'='*60}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    migrate_data()