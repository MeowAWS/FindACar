import requests
from bs4 import BeautifulSoup
from bson import ObjectId
from database import setup_db,setup_db_1,setup_db_2

def search_records(brand, name, price, condition_label):
    collection, db = setup_db()
# this is the list of steps mongodb run one by one 
    pipeline = [
        # Join brands
        {
            "$lookup": {
                "from": "brands", #see the collection brand in the db auto_search
                "localField": "brand",#field in current collection (cars collection)
                "foreignField": "_id",# fields in the brand collection foreign key 
                "as": "brand_info"#output field name
            }
        },
        {"$unwind": "$brand_info"},

        # Join models
        {
            "$lookup": {
                "from": "models",
                "localField": "name",   # name now contains model ObjectId
                "foreignField": "_id",
                "as": "model_info"
            }
        },
        {"$unwind": "$model_info"},

        # Apply filters
        {
            "$match": {
                "brand_info.name": {"$regex": brand, "$options": "i"},
                "model_info.name": {"$regex": name, "$options": "i"},
                "condition_label": condition_label,
                "price": {"$lte": int(price)}
            }
        },

        # Final shape for frontend
        {
            "$project": {
                "_id": 0,
                "url": "$URL",
                "brand": "$brand_info.name",
                "name": "$model_info.name",
                "price": 1,
                "condition": "$condition_label",
                "image": { "$arrayElemAt": ["$images", 0] }
            }
        }
    ]

    results = collection.aggregate(pipeline)
    return list(results)




#validates if the ad. still exist or now 
def pechay_say_ADS_lao(brand,name,price,condition_label):
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

def get_all_the_brands():
    
    collection,db=setup_db_1()
    brands = collection.find({}, {"_id": 0, "name": 1})
    return [b["name"] for b in brands]

def get_all_names(brand):
    #set db and collection 
    brand_col,model_col,db=setup_db_2()
    #find brand document
    brand_doc=brand_col.find_one(
        {"name":{"$regex":f"^{brand}$","$options":"i"}}
    )
    #if not find just return empty array
    if not brand_doc:
        return[]
    
    brand_id=brand_doc["_id"]
    #finds all the names for the given brand
    models=model_col.find(
        {"brand":brand_id},
        {"_id":0,"name":1}
    ).sort("name",1)
    
    return[m["name"] for m in models]