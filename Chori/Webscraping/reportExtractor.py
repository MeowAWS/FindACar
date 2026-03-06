import os
import requests
from bs4 import BeautifulSoup

BASE = "https://www.pakwheels.com"

cars_dir = "cars"
output_dir = "inspections"

os.makedirs(output_dir, exist_ok=True)

headers = {
    "User-Agent": "Mozilla/5.0",
}

session = requests.Session()
session.headers.update(headers)

print("\n=== STARTING RETRIEVER ===\n")

report_count = 1

files = sorted(os.listdir(cars_dir))

for file in files:
    if not file.endswith(".html"):
        continue

    file_path = os.path.join(cars_dir, file)
    print(f"[READING] {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    link = soup.find("a", string="View Full Inspection Report")

    if not link:
        print("[INFO] No inspection report found")
        continue

    href = link.get("href")
    full_url = BASE + href

    print(f"[FETCHING] {full_url}")

    try:
        r = session.get(full_url, timeout=10)

        if r.status_code != 200:
            print("[WARNING] Failed to fetch report")
            continue

        save_path = os.path.join(output_dir, f"report_{report_count}.html")

        with open(save_path, "w", encoding="utf-8") as out:
            out.write(r.text)

        print(f"[SAVED] {save_path}")

        report_count += 1

    except Exception as e:
        print(f"[ERROR] {e}")

print("\n=== RETRIEVAL COMPLETE ===")