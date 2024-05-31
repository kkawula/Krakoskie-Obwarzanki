from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from server.database import init
from server.models.shop import Shop
from server.models.shop import ShopsByDistance
from server.models.shop import ShopsByNumber

app = FastAPI()

origins = [
    # "http://localhost",
    # "http://localhost:5173",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def start_db():
    await init()


@app.get("/", tags=["Root"])
async def root():
    return RedirectResponse(url="/docs")


@app.get("/shops", tags=["Shops"])
async def all_shops():
    return await Shop.all().to_list()


@app.post("/shops", tags=["Shops"])
async def create_shop(shop: Shop):
    await shop.insert()
    return shop


@app.get("/shops/{shop_id}", tags=["Shops"])
async def get_shop(shop_id: str):
    shop = await Shop.get(shop_id)
    return shop


@app.post("/shops/by_distance", tags=["Shops"])
async def get_shops_by_dist(query: ShopsByDistance):
    r = query.r
    lat = query.lat
    long = query.long

    geo_near_stage = {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [lat, long]},
            "spherical": True,
            "distanceField": "distance",
            "maxDistance": r,
        }
    }

    result = await Shop.get_motor_collection().aggregate([geo_near_stage]).to_list(None)

    shops = [Shop(**doc) for doc in result]
    return [shop.dict() for shop in shops]


@app.post("/shops/by_number", tags=["Shops"])
async def get_n_nearest_shops(query: ShopsByNumber):
    n = query.n
    lat = query.lat
    long = query.long

    geo_near_stage = {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [lat, long]},
            "spherical": True,
            "distanceField": "distance",
        }
    }

    result = await Shop.get_motor_collection().aggregate([geo_near_stage]).to_list(n)

    shops = [Shop(**doc) for doc in result]
    return [shop.dict() for shop in shops]
