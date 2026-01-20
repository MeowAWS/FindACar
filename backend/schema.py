import requests
from bs4 import BeautifulSoup
from bson import ObjectId
from database import setup_db

def search_records(brand,name,price,condition_label):
    collection,db=setup_db(brand)
    query={
        "name":{"$regex":name,"$options":"i"},#partial match wsay zaroort nai lkin for the safer side
        "condition_label":condition_label,#match condition label
        "price":{"$lte":int (price)}#price from 0 to price
    }
    #run query and get all the results
    results=collection.find(query)
    #format into json
    output=[]
    for doc in results:
        output.append({
            "url":doc.get("URL"),
            "brand":doc.get("brand"),
            "name":doc.get("name"),
            "price":doc.get("price"),
            "image":doc.get("images",[None])[0],#first image
            "condition":doc.get("condition_label")
        })
    return output


def check_add_exist(brand,name,price,condition_label):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/used-cars/honda/32"
    }
    ads = search_records(brand, name, price, condition_label)

    valid_ads = []

    for ad in ads:
        url = ad["url"]
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200:
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            # This text appears when ad is expired
            if "This ad is no longer active" in soup.text:
                continue  # skip expired ad
            # Otherwise it's valid
            valid_ads.append(ad)
        except Exception:
            continue
    return valid_ads