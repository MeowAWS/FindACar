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
def setup_db_1():
    db = client["auto_shop"]
    collection = db["brands"]
    return collection, db
def setup_db_2():
    db = client["auto_shop"]
    brands_col,models_col= db["brands"],db["models"]
    return brands_col,models_col,db