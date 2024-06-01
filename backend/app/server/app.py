from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from server.database import init
from server.models.shop import Shop, ShopWithDistance
from server.models.query import Query
from server.models.utils import Point

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
async def get_shops_by_dist(query: Query.ShopsByDistanceQuery):
    radius = query.r
    point = Point(coordinates=[query.lat, query.long])

    shops = await Shop.aggregate(
        [
            {
                "$geoNear": {
                    "near": point.dict(),
                    "distanceField": "distance",
                    "maxDistance": radius,
                }
            }
        ], projection_model=ShopWithDistance
    ).to_list()
    return shops


@app.post("/shops/by_number", tags=["Shops"])
async def get_n_nearest_shops(query: Query.ShopsByNumber):
    n = query.n
    point = Point(coordinates=[query.lat, query.long])

    shops = await Shop.aggregate(
        [
            {
                "$geoNear": {
                    "near": point.dict(),
                    "distanceField": "distance",
                }
            }
        ], projection_model=ShopWithDistance
    ).to_list(n)

    return shops
