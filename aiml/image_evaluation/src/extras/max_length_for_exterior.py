from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# MongoDB connection settings
MONGO_URI = os.getenv("DB_URL")
DATABASE_NAME = ("Honda_cars")
COLLECTION_NAME = ("listings")

def find_max_exterior_images():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Find all documents that have damage_labels
    query = {"damage_labels": {"$exists": True}}
    documents = collection.find(query)
    
    max_length = 0
    max_doc_id = None
    total_docs = 0
    
    for doc in documents:
        total_docs += 1
        
        # Get the length of exterior_images
        if 'exterior_images' in doc and doc['exterior_images'] is not None:
            current_length = len(doc['exterior_images'])
            
            if current_length > max_length:
                max_length = current_length
                max_doc_id = doc.get('_id')
                
            print(f"Document _id: {doc['_id']}, Exterior images count: {current_length}")
    
    print(f"\n{'='*60}")
    print(f"Total documents with damage_labels: {total_docs}")
    print(f"Maximum exterior_images length: {max_length}")
    print(f"Document with max length: {max_doc_id}")
    print(f"{'='*60}")
    
    # Close the connection
    client.close()
    
    return max_length

if __name__ == "__main__":
    max_length = find_max_exterior_images()