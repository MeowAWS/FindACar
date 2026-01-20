from pymongo import MongoClient
import os
from dotenv import load_dotenv

#calling function to setup db
def setup_db(brand):
    load_dotenv()
    db_url=os.getenv("DB_URL")
    client=MongoClient(db_url)
    if brand=="Toyota":
        db_name=client["Toyota_cars_2"]
    elif brand=="Honda":
        db_name=client["Honda_cars_2"]
    else:
        db_name=client["Suzuki_cars_2"]
    collection=db_name["listings"]
    return collection,db_name
