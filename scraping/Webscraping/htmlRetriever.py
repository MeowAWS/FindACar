import os
import requests

os.makedirs("pages", exist_ok=True)

url = "https://www.pakwheels.com/carsure-reports/b447f4834f3d90167bfa5f3630785e3f"

headers = {
    "User-Agent": "Mozilla/5.0",
}

r = requests.get(url, headers=headers)

with open("pages/report.html", "w", encoding="utf-8") as f:
    f.write(r.text)
    print("Written")
