from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
db_url=os.getenv("DB_URL")
client=MongoClient(db_url)
DATABASES = {
    "toyota": "Toyota_cars_2",
    "honda": "Honda_cars_2",
    "suzuki": "Suzuki_cars_2"
    }
#calling function to setup db
def setup_db(brand: str):
    brand = brand.lower()

    if brand not in DATABASES:
        raise ValueError("Invalid brand")

    db = client[DATABASES[brand]]
    collection = db["listings"]

    return collection