import os
import requests
import time
import random
import BeautifulSoup

os.makedirs("pages", exist_ok=True)


def extract_ads_link_and_title_fromhtml():
    urls=[]
    titles=[]
    for i in range (1,90):
        with open(f"pages/page_{i}.html","r",encoding="utf-8") as f:
            html=f.read()
        soup=BeautifulSoup(html,'html.parser')
        script_tag=soup.find("script", type="application/ld+json")
        data =json.loads(script_tag.string)
        listings=data.get("itemListElement", [])
        for j in listings:
            urls.append(j.get("url"))
            titles.append(j.get("title"))
        print(urls)
        print(titles)
    return urls, titles

extract_ads_link_and_title_fromhtml()

# base_url = "https://www.pakwheels.com/used-cars/suzuki/32"
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
#     "Accept-Language": "en-US,en;q=0.9",
#     "Referer": "https://www.pakwheels.com/used-cars/suzuki/32"
# }

# for page in range(1, 90):  # first 90 pages
#     url = f"{base_url}?page={page}&_pjax=%5Bdata-pjax-container%5D"
#     r = requests.get(url, headers=headers)
#     with open(f"pages/page_{page}.html", "w", encoding="utf-8") as f:
#         f.write(r.text)
#     time.sleep(1 + 2 * random.random())