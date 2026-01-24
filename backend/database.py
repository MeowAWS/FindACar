from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()
db_url=os.getenv("DB_URL")
client=MongoClient(db_url)
#calling function to setup db
def setup_db():
    db = client["auto_shop"]
    collection = db["cars"]
    return collection, db