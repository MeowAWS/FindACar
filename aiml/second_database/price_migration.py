from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
SOURCE_DATABASE = "Honda_cars"
SOURCE_COLLECTION = "listings"
TARGET_DATABASE = "Honda_cars_2"
TARGET_COLLECTION = "listings"

def update_price_field():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    
    # Source database and collection
    source_db = client[SOURCE_DATABASE]
    source_collection = source_db[SOURCE_COLLECTION]
    
    # Target database and collection
    target_db = client[TARGET_DATABASE]
    target_collection = target_db[TARGET_COLLECTION]
    
    # Find all documents that have primary_key and price
    query = {"primary_key": {"$exists": True}, "price": {"$exists": True}}
    documents = source_collection.find(query).sort("primary_key", 1)
    
    updated_count = 0
    not_found_count = 0
    skipped_count = 0
    
    for doc in documents:
        primary_key = doc.get("primary_key")
        price = doc.get("price")
        
        # Check if document exists in target collection
        target_doc = target_collection.find_one({"primary_key": primary_key})
        
        if target_doc:
            # Update only the price field
            result = target_collection.update_one(
                {"primary_key": primary_key},
                {"$set": {"price": price}}
            )
            
            if result.modified_count > 0:
                updated_count += 1
                print(f"Updated primary_key: {primary_key} with price: {price}")
            else:
                skipped_count += 1
                print(f"Skipped primary_key: {primary_key} (price already exists or unchanged)")
        else:
            not_found_count += 1
            print(f"Warning: primary_key {primary_key} not found in target database")
    
    print(f"\n{'='*60}")
    print(f"Price Update Complete!")
    print(f"Documents updated: {updated_count}")
    print(f"Documents skipped (unchanged): {skipped_count}")
    print(f"Documents not found in target: {not_found_count}")
    print(f"Source: {SOURCE_DATABASE}.{SOURCE_COLLECTION}")
    print(f"Target: {TARGET_DATABASE}.{TARGET_COLLECTION}")
    print(f"{'='*60}")
    
    # Close the connection
    client.close()

if __name__ == "__main__":
    update_price_field()