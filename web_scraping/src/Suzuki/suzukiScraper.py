import os
import requests
import time
import random

os.makedirs("pages", exist_ok=True)

base_url = "https://www.pakwheels.com/used-cars/suzuki/32"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/used-cars/suzuki/32"
}

for page in range(1, 90):  # first 90 pages
    url = f"{base_url}?page={page}&_pjax=%5Bdata-pjax-container%5D"
    r = requests.get(url, headers=headers)
    with open(f"pages/page_{page}.html", "w", encoding="utf-8") as f:
        f.write(r.text)
    time.sleep(1 + 2 * random.random())