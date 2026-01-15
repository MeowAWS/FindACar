import requests
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()
db_url = os.getenv("DB_URL")

# Connect to MongoDB
client = MongoClient(db_url)
db = client["Suzuki_cars"]
collection = db["listings"]

def display_image(url, headers):
    """Download and display image from URL"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        
        plt.figure(figsize=(10, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Image URL: {url[:50]}...")
        plt.tight_layout()
        plt.show()
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to display image: {e}")
        return False

def review_exterior_images():
    """Main function to review and filter exterior images"""
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.pakwheels.com/"
    }
    
    # Get all documents with exterior images
    docs_with_exterior = list(collection.find(
        {"exterior_images": {"$exists": True, "$ne": []}},
        {"_id": 1, "exterior_images": 1}
    ))
    
    print(f"Found {len(docs_with_exterior)} documents with exterior images")
    
    total_reviewed = 0
    total_removed = 0
    
    for doc in docs_with_exterior:
        doc_id = doc["_id"]
        exterior_images = doc.get("exterior_images", [])
        
        if not exterior_images:
            continue
        
        print(f"\n{'='*60}")
        print(f"Document ID: {doc_id}")
        print(f"Total exterior images: {len(exterior_images)}")
        print(f"{'='*60}")
        
        images_to_keep = []
        
        for idx, img_url in enumerate(exterior_images):
            print(f"\n[{idx + 1}/{len(exterior_images)}] Displaying image...")
            
            # Display the image
            if not display_image(img_url, headers):
                print("Skipping due to display error...")
                continue
            
            # Get user input
            while True:
                response = input("Is this an EXTERIOR image? (Enter=yes/Space=no/s=skip/q=quit): ").strip()
                
                if response == '' or response.lower() == 'y':  # Enter key or 'y'
                    images_to_keep.append(img_url)
                    print("✓ Keeping image in exterior")
                    total_reviewed += 1
                    break
                elif response == ' ' or response.lower() == 'n':  # Space key or 'n'
                    print("✗ Removing image from exterior")
                    total_reviewed += 1
                    total_removed += 1
                    break
                elif response.lower() == 's':
                    images_to_keep.append(img_url)
                    print("→ Skipping (keeping by default)")
                    break
                elif response.lower() == 'q':
                    print("\n[QUIT] Saving progress and exiting...")
                    # Update current document before quitting
                    if images_to_keep != exterior_images:
                        collection.update_one(
                            {"_id": doc_id},
                            {"$set": {"exterior_images": images_to_keep}}
                        )
                    print(f"\nTotal reviewed: {total_reviewed}")
                    print(f"Total removed: {total_removed}")
                    return
                else:
                    print("Invalid input. Please press Enter (yes), Space (no), 's' (skip), or 'q' (quit)")
        
        # Update the document if changes were made
        if images_to_keep != exterior_images:
            collection.update_one(
                {"_id": doc_id},
                {"$set": {"exterior_images": images_to_keep}}
            )
            print(f"\n✓ Updated document {doc_id}")
            print(f"  Kept: {len(images_to_keep)}/{len(exterior_images)} images")
    
    print(f"\n{'='*60}")
    print("REVIEW COMPLETE!")
    print(f"Total images reviewed: {total_reviewed}")
    print(f"Total images removed: {total_removed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    print("Starting Exterior Image Review Tool...")
    print("Instructions:")
    print("  - Press ENTER to keep the image as exterior")
    print("  - Press SPACE to remove the image from exterior")
    print("  - Press 's' to skip (keep by default)")
    print("  - Press 'q' to quit and save progress")
    print()
    
    review_exterior_images()
    
    print("\nClosing database connection...")
    client.close()
    print("Done!")