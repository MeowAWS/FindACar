from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from schema import pechay_say_ADS_lao,get_all_the_brands,get_all_names

app = FastAPI()


app.add_middleware(         #dadi amma jo baat manwati hein
    CORSMiddleware,
    allow_origins=["*"],            #do this when url ready for our website allow_origins=["http://localhost:3000"]
                                    #currnetly it allows all websites to call api
    allow_credentials=True,
    allow_methods=["*"],            #miss karao
    allow_headers=["*"],            #inspect > network > ctrl + r > headers (jis sy pakwheels scrap kia)
)
@app.get("/")
def home():
    return {"message": "API is running"}


@app.get("/search")
async def search(       #asyn run code block by block, a single waiter can cater multiple customers at the same time
    brand: str = Query(...),
    name: str = Query(...),
    price: int = Query(...),
    condition: str = Query(...)
):
    results = pechay_say_ADS_lao(brand, name, price, condition)
    return {"results": results}


@app.get("/brands")
async def get_brands():
    return{"brands":get_all_the_brands()}

@app.get("/names")
async def get_names(brand:str):
    return{"Car_name":get_all_names(brand)}


print ("kam kr lo bhai plzzzzzzzzzzzzzzzzzzzzzzzzzz")
print ("tension na lo subi bhai")