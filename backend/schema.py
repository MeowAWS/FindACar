import requests
from bs4 import BeautifulSoup
from bson import ObjectId
from database import setup_db,setup_db_1,setup_db_2
from datetime import datetime,timezone



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
                "image": { "$arrayElemAt": ["$images", 0] },
                "is_active": 1
            }
        }
    ]

    results = collection.aggregate(pipeline)
    return list(results)




#validates if the ad. still exist or now 
def pechay_say_ADS_lao(brand, name, price, condition_label):
    ads = search_records(brand, name, price, condition_label)

    valid_ads = [ad for ad in ads if ad.get("is_active") is True]

    return valid_ads


def validate_ads_and_update():
    collection, db = setup_db()

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/used-cars/honda/32"
    }

    # Fetch all ads from DB
    ads = collection.find({}, {"_id": 1, "URL": 1})

    for ad in ads:
        ad_id = ad["_id"]
        url = ad.get("URL")

        if not url:
            continue

        is_active = True

        try:
            response = requests.get(url, headers=headers, timeout=5)

            if response.status_code != 200:
                is_active = False
            else:
                soup = BeautifulSoup(response.text, "html.parser")
                if "This ad is no longer active" in soup.text:
                    is_active = False

        except Exception:
            is_active = False

        # ✅ Update DB (this is the important part)
        collection.update_one(
            {"_id": ad_id},
            {
                "$set": {
                    "is_active": is_active,
                    "last_checked": datetime.now(timezone.utc)
                }
            }
        )

    print("Validation completed.")


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