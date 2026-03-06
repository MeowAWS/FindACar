import requests
from bs4 import BeautifulSoup
import os
import time

BASE = "https://www.pakwheels.com"

os.makedirs("cars", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
}

session = requests.Session()
session.headers.update(headers)

car_links = []

print("\n=== STARTING SCRAPER ===\n")

# Step 1: collect car URLs
for page in range(1, 59):
    url = f"https://www.pakwheels.com/used-cars/search/-/cert_pakwheels-inspected/?page={page}"

    print(f"[PAGE] Fetching listing page {page} -> {url}")

    try:
        r = session.get(url, timeout=10)
        print(f"[STATUS] Page {page} status code: {r.status_code}")

        if r.status_code != 200:
            print("[WARNING] Page request failed, skipping")
            continue

        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.select("a.car-name")

        print(f"[INFO] Found {len(links)} cars on page {page}")

        for a in links:
            href = a.get("href")
            if href:
                car_links.append(BASE + href)

    except Exception as e:
        print(f"[ERROR] Failed to fetch page {page}: {e}")

print(f"\n[TOTAL] Total car links collected: {len(car_links)}\n")


# Step 2: download car pages
for i, link in enumerate(car_links[:5000]):
    print(f"[DOWNLOAD] ({i+1}/{min(5000, len(car_links))}) Fetching: {link}")

    try:
        r = session.get(link, timeout=10)
        print(f"[STATUS] Response code: {r.status_code}")

        if r.status_code != 200:
            print("[WARNING] Failed to fetch page, skipping")
            continue

        file_path = f"cars/car_{i}.html"

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(r.text)

        print(f"[SAVED] {file_path}")

    except Exception as e:
        print(f"[ERROR] Failed to download {link}: {e}")

    time.sleep(1)

print("\n=== SCRAPING COMPLETE ===")