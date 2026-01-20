from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from schema import search_cars

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            #do this when url ready for our website allow_origins=["http://localhost:3000"]
                                    #currnetly it allows all websites to call api
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
def search(
    brand: str = Query(...),
    name: str = Query(...),
    price: int = Query(...),
    condition: str = Query(...)
):
    results = search_cars(brand, name, price, condition)
    return {"results": results}
