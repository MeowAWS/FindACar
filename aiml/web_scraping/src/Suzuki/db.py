# %%
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import json
import os
import re
# -------------------- Load environment --------------------
mongo_url = "" ####ENTER YOUR URL I AM NOT DOING ITT FOR YOU

client = MongoClient(mongo_url)
data_base = client["Suzuki_cars"]         # database
collection = data_base["listings"]        # collection/table

# -------------------- Scraper --------------------
def extract_listings(listings_dir="listings"):
    listings = []
   
    files = sorted(os.listdir(listings_dir),
           key=lambda x: int(re.search(r'(\d+)', x).group()))
    print(f"[INFO] Found {len(files)} HTML files in '{listings_dir}'")

    for idx, file in enumerate(files, 1):
        print(f"[INFO] Processing file {idx}/{len(files)}: {file}")
        try:
            with open(os.path.join(listings_dir, file), "r", encoding="utf-8") as f:
                html = f.read()

            soup = BeautifulSoup(html, "html.parser")

            # Defaults
            brand = name = description = price = url = title = None
            images = []
            rating = None

            # ---------- JSON-LD ----------
            jsonld_found = False
            for tag in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(tag.string)
                    if isinstance(data, dict) and ("Product" in data.get("@type", []) or data.get("@type") == "Product"):
                        brand = data.get("brand", {}).get("name")
                        name = data.get("model")
                        description = data.get("description")
                        price = data.get("offers", {}).get("price")
                        url = data.get("offers", {}).get("url") or data.get("url")
                        title = data.get("name")
                        jsonld_found = True
                        break
                except (json.JSONDecodeError, TypeError):
                    continue
            if not jsonld_found:
                print(f"[WARN] No valid JSON-LD found in file: {file}")

            # ---------- Images ----------
            gallery = soup.find("ul", class_="gallery")
            if gallery:
                for li in gallery.find_all("li"):
                    img = li.find("img")
                    if img:
                        src = img.get("data-original") or img.get("src")
                        if src:
                            images.append(src)
            print(f"[INFO] Found {len(images)} images")

            # ---------- Inspection rating ----------
            rating_div = soup.find("div", class_="right pull-right primary-lang")
            if rating_div:
                try:
                    text = rating_div.text.strip()
                    score = float(text.split("/")[0])
                    rating = int(round(score))
                except (ValueError, IndexError):
                    pass

            # ---------- Final document ----------
            listings.append({
                "URL": url,
                "Title": title,
                "brand": brand,
                "name": name,
                "description": description,
                "images": images,
                "rating": rating,
                "price": price
            })

        except Exception as e:
            print(f"[ERROR] Failed to process file {file}: {e}")
            listings.append({
                "URL": None,
                "Title": None,
                "brand": None,
                "name": None,
                "description": None,
                "images": [],
                "rating": None,
                "price": None
            })

    return listings

# -------------------- Run Extraction --------------------
listings = extract_listings()

# Remove empty/broken listings
listings = [l for l in listings if l["URL"] or l["Title"]]

# Insert into MongoDB
if listings:
    collection.insert_many(listings)

print(f"[INFO] {len(listings)} listings inserted into MongoDB")
# %%
