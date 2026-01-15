# %%
import clip #for model classification
import torch
from PIL import Image
import requests
from pymongo import MongoClient
from io import BytesIO
from tqdm import tqdm#lib to show progress


# %%
from dotenv import load_dotenv
import os

# %%
load_dotenv()
db_url=os.getenv("DB_URL")

# %%
client = MongoClient(db_url)
db= client["Suzuki_cars"]
collection = db["listings"]


# %%
def set_clip_function():
    LABELS = [
    "a clear photo of a car exterior (outside view of car)",
    "a clear photo of a car interior (seats, dashboard, cabin)",
    "a clear photo of a car engine bay",
    "a photo of car key or keychain",
    "a random, unclear, blurry, unrelated or unidentified photo"
]

    CATEGORY_FIELDS = {
    0: "exterior_images",
    1: "interior_images",
    2: "engine_images",
    3: "key_images",
    4: "unidentified_images"
}


    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    text_tokens = clip.tokenize(LABELS).to(device)
    session=requests.Session()
    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/used-cars/honda/32"
}

    return LABELS,CATEGORY_FIELDS,device,model,preprocess,text_tokens,session,headers

# %%
LABELS,CATEGORY_FIELDS,device,model,preprocess,text_tokens,session,headers=set_clip_function()

# %%
def classify_image_url(
    url,
    model,
    preprocess,
    text_tokens,
    labels,
    device,
    headers,
    session,
    confidence_threshold=0.5
):
    try:
        response = session.get(url,headers=headers, timeout=10)
        response.raise_for_status()

        img = Image.open(BytesIO(response.content)).convert("RGB")
        image_tensor = preprocess(img).unsqueeze(0).to(device)

        with torch.no_grad():
            image_features = model.encode_image(image_tensor)
            text_features = model.encode_text(text_tokens)
            similarity = (image_features @ text_features.T).softmax(dim=-1)

        best_idx = similarity.argmax().item()
        confidence = similarity[0][best_idx].item()
        label = labels[best_idx]

        if confidence < confidence_threshold:
            return None, confidence

        return label, confidence

    except Exception as e:
        print(f"[ERROR] Failed on {url}: {e}")
        return None, 0.0


# %%
def process_documents(
    collection,
    model,
    preprocess,
    text_tokens,
    labels,
    device,
    headers,
    session,
):
    print("Fetching document IDs...")
    
    all_ids = [
        doc["_id"] 
        for doc in collection.find(
            {"images": {"$exists": True}}, 
            {"_id": 1}
        )
    ]
    print(f"Found {len(all_ids)} documents to process")
    for doc_id in tqdm(all_ids, desc="Processing documents"):
        doc = collection.find_one({"_id": doc_id})
        if not doc:
            continue

        # Create empty buckets for all categories
        categorized = {field: [] for field in CATEGORY_FIELDS.values()}

        for url in doc.get("images", []):
            label, conf = classify_image_url(
                url=url,
                model=model,
                preprocess=preprocess,
                text_tokens=text_tokens,
                labels=labels,
                device=device,
                headers=headers,
                session=session
            )

            if label is None:
                continue

            # Find index of predicted label
            idx = labels.index(label)

            # Get correct Mongo field
            mongo_field = CATEGORY_FIELDS[idx]

            categorized[mongo_field].append(url)

        # Save everything in the same document
        collection.update_one(
            {"_id": doc_id},
            {"$set": categorized}
        )

    print("✅ Processing completed.")


# %%
process_documents(collection,model,preprocess,text_tokens,LABELS,device,headers,session)


# %%



