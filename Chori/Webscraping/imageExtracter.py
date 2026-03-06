import re
import json
import os
from bs4 import BeautifulSoup

TARGET_A = {"A1", "A2"}
TARGET_U = {"U1", "U2"}

a_images = set()
u_images = set()
table_images = set()

folder = "inspections"

print("\n=== STARTING PARSER ===\n")

# Sort numerically instead of lexicographically
files = sorted(
    (f for f in os.listdir(folder) if f.endswith(".html")),
    key=lambda x: int(re.search(r'(\d+)', x).group())
)

for file in files:

    path = os.path.join(folder, file)
    print(f"[PROCESSING] {file}")

    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    # -------------------------
    # PART 1: Extract A1/A2/U1/U2 defect images
    # -------------------------
    for match in re.finditer(r'\{[^{}]*"key":"(A1|A2|U1|U2)"[^{}]*\}', html):
        try:
            obj = json.loads(match.group())
            if "original" in obj and obj["original"]:  # filter None
                if obj["key"] in TARGET_A and len(a_images) < 1300:
                    a_images.add(obj["original"])
                elif obj["key"] in TARGET_U and len(u_images) < 1300:
                    u_images.add(obj["original"])
        except:
            pass

    # -------------------------
    # PART 2: Extract table defect images
    # -------------------------
    soup = BeautifulSoup(html, "html.parser")
    defected_tds = soup.find_all("td", class_="bg-carsure-danger")

    for td in defected_tds:

        if len(table_images) >= 1300:
            break

        prev_td = td.find_previous_sibling("td", id="overlay_pic")

        if prev_td:
            i_tag = prev_td.find("i", {"data-gallery": True})

            if i_tag:
                gallery_json = i_tag["data-gallery"].replace("&quot;", '"')

                try:
                    images = json.loads(gallery_json)
                    for img in images:
                        src = img.get("src")
                        if src:  # filter None
                            if len(table_images) < 1300:
                                table_images.add(src)
                except json.JSONDecodeError:
                    pass

# -------------------------
# WRITE FILES
# -------------------------
with open("scratch.txt", "w") as f:
    for url in a_images:
        if url:
            f.write(url + "\n")

with open("dent.txt", "w") as f:
    for url in u_images:
        if url:
            f.write(url + "\n")

with open("lamp_broken.txt", "w") as f:
    for url in table_images:
            f.write(url + "\n")

print("\nSaved:")
print("Scratch:", len(a_images))
print("Dent:", len(u_images))
print("Lamp_Broken:", len(table_images))