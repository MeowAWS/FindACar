from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from schema import pechay_say_ADS_lao, get_all_the_brands, get_all_names

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "API is running"}

@app.get("/search")
async def search(
    brand: str = Query(...),
    name: str = Query(...),
    price: int = Query(...),
    condition: str = Query(...)
):
    results = pechay_say_ADS_lao(brand, name, price, condition)
    return {"results": results}

@app.get("/brands")
async def get_brands():
    return {"brands": get_all_the_brands()}

@app.get("/names")
async def get_names(brand: str):
    return {"Car_name": get_all_names(brand)}

# ✅ Add this route
@app.get("/conditions")
async def get_conditions():
    # You can replace this with your DB query later
    return {"conditions": ["A+", "A", "B+", "B", "C+", "C"]}

print("kam kr lo bhai plzzzzzzzzzzzzzzzzzzzzzzzzzz")
print("tension na lo subi bhai")
