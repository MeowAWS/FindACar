import os
import requests
import time
import random

os.makedirs("listings", exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/"
}

def scrape_listing(url, count):
    try:
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            print("Failed:", url, r.status_code)
            return

        fname = f"listing_{count}.html"  # sequential listing filename
        with open(f"listings/{fname}", "w", encoding="utf-8") as f:
            f.write(r.text)

        print("Saved:", fname, url)

    except Exception as e:
        print("Error:", url, e)


def read_and_scrape_listings():
    with open("urls.txt", "r", encoding="utf-8") as f:
        for count, line in enumerate(f, start=1):  # start numbering from 1
            url = line.strip()
            if not url:
                continue

            scrape_listing(url, count)
            time.sleep(1 + 2 * random.random())


read_and_scrape_listings()

