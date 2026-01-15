import os
import requests
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')  # Non-blocking backend

# Load environment variables
load_dotenv()
db_url = os.getenv("DB_URL")

# Connect to MongoDB
client = MongoClient(db_url)
db = client["Suzuki_cars"]
collection = db["listings"]

def display_image(url, headers, fig):
    """Download and display image from URL in the same figure"""
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        
        fig.clf()  # Clear previous content
        plt.imshow(img)
        plt.axis('off')
        plt.title(f"Image URL: {url[:50]}...")
        plt.tight_layout()
        plt.draw()
        plt.pause(0.1)  # brief pause to render
        
        return True
    except Exception as e:
        print(f"[ERROR] Failed to display image: {e}")
        return False

def get_listing_numbers():
    """Prompt user to enter listing numbers to review"""
    print("\n" + "="*60)
    print("Enter listing numbers to review (one per line)")
    print("Press 'q' when done entering numbers")
    print("="*60)
    
    listing_numbers = []
    while True:
        user_input = input("Enter listing number (or 'q' to finish): ").strip()
        if user_input.lower() == 'q':
            break
        
        try:
            num = int(user_input)
            if num > 0:
                listing_numbers.append(num)
                print(f"  ✓ Added listing #{num}")
            else:
                print("  ✗ Please enter a positive number")
        except ValueError:
            print("  ✗ Invalid input. Please enter a number or 'q'")
    
    return listing_numbers

def review_exterior_images(specific_listings=None):
    """Main function to review and filter exterior images (one image at a time)"""
    
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
    
    # Filter to specific listings if provided
    if specific_listings:
        print(f"\nFiltering to {len(specific_listings)} specific listings: {specific_listings}")
        docs_to_review = [doc for i, doc in enumerate(docs_with_exterior, start=1) if i in specific_listings]
        print(f"Will review {len(docs_to_review)} documents")
    else:
        docs_to_review = docs_with_exterior
    
    total_reviewed = 0
    total_removed = 0

    # Initialize a single figure for all images
    fig = plt.figure(figsize=(10, 8))
    
    for doc_index, doc in enumerate(docs_to_review, start=1):
        doc_id = doc["_id"]
        exterior_images = doc.get("exterior_images", [])
        
        if not exterior_images:
            continue

        # Find original listing number
        original_index = docs_with_exterior.index(doc) + 1

        print(f"\n{'='*60}")
        print(f"Reviewing listing #{original_index} ({doc_index}/{len(docs_to_review)})")
        print(f"Document ID: {doc_id}")
        print(f"Total exterior images: {len(exterior_images)}")
        print(f"{'='*60}")

        images_to_keep = []

        # Review images one by one in the same figure
        for idx, img_url in enumerate(exterior_images):
            print(f"\n[{idx + 1}/{len(exterior_images)}] Displaying image...")
            
            success = display_image(img_url, headers, fig)
            if not success:
                print("Skipping due to display error...")
                continue
            
            # Get user input
            while True:
                response = input("Is this an EXTERIOR image? (Enter=yes/n=no/s=skip/q=quit): ").strip()
                if response == '' or response.lower() == 'y':
                    images_to_keep.append(img_url)
                    total_reviewed += 1
                    break
                elif response.lower() == 'n':
                    total_reviewed += 1
                    total_removed += 1
                    break
                elif response.lower() == 's':
                    images_to_keep.append(img_url)
                    break
                elif response.lower() == 'q':
                    print("\n[QUIT] Saving progress and exiting...")
                    if images_to_keep != exterior_images:
                        collection.update_one({"_id": doc_id}, {"$set": {"exterior_images": images_to_keep}})
                    print(f"Total reviewed: {total_reviewed}")
                    print(f"Total removed: {total_removed}")
                    return
                else:
                    print("Invalid input. Press Enter (yes), 'n' (no), 's' (skip), or 'q' (quit).")
        
        # Update document if changes were made
        if images_to_keep != exterior_images:
            collection.update_one({"_id": doc_id}, {"$set": {"exterior_images": images_to_keep}})
            print(f"\n✓ Updated document {doc_id}")
            print(f"  Kept: {len(images_to_keep)}/{len(exterior_images)} images")
    
    print(f"\n{'='*60}")
    print("REVIEW COMPLETE!")
    print(f"Total images reviewed: {total_reviewed}")
    print(f"Total images removed: {total_removed}")
    print(f"{'='*60}")

if __name__ == "__main__":
    print("Starting Exterior Image Review Tool...")
    print("\nOptions:")
    print("  1. Review specific listings (enter numbers)")
    print("  2. Review all listings")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    specific_listings = None
    if choice == '1':
        specific_listings = get_listing_numbers()
        if not specific_listings:
            print("\nNo listing numbers entered. Exiting...")
            client.close()
            exit()
        print(f"\nWill review {len(specific_listings)} specific listings")
    elif choice == '2':
        print("\nWill review all listings")
    else:
        print("\nInvalid choice. Exiting...")
        client.close()
        exit()
    
    print("\nInstructions:")
    print("  - Press ENTER to keep the image as exterior")
    print("  - Press 'n' to remove the image from exterior")
    print("  - Press 's' to skip (keep by default)")
    print("  - Press 'q' to quit and save progress")
    print()
    
    plt.ion()  # Interactive mode
    review_exterior_images(specific_listings)
    
    plt.close('all')  # Close all figures
    print("\nClosing database connection...")
    client.close()
    print("Done!")