from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from server.database import init_db
from server.models.query import Query
from server.models.shop import Shop, ShopWithDistance, ShopWithPosition
from server.models.utils import Point


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


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


@app.get("/", tags=["Root"])
async def root():
    return RedirectResponse(url="/docs")


@app.get("/shops", tags=["Shops"], response_model=list[ShopWithPosition])
async def all_shops():
    shops = await Shop.all().to_list()
    return shops


@app.post("/shops", tags=["Shops"], response_model=ShopWithPosition)
async def create_shop(shop: ShopWithPosition):
    await shop.insert()
    return shop


@app.get("/shops/{shop_id}", tags=["Shops"], response_model=ShopWithPosition)
async def get_shop(shop_id: str):
    shop = await Shop.get(shop_id)
    return shop


@app.post("/shops/by_distance", tags=["Shops"], response_model=list[ShopWithDistance])
async def get_shops_by_dist(query: Query.ShopsByDistance):
    radius = query.radius
    point = Point(**query.model_dump())

    return await Shop.aggregate(
        [
            {
                "$geoNear": {
                    "near": point.model_dump(),
                    "distanceField": "distance",
                    "maxDistance": radius,
                }
            }
        ],
        projection_model=ShopWithDistance,
    ).to_list()


@app.post("/shops/by_number", tags=["Shops"], response_model=list[ShopWithDistance])
async def get_n_nearest_shops(query: Query.ShopsByNumber):
    n = query.n_closest
    point = Point(**query.model_dump())

    return await Shop.aggregate(
        [
            {
                "$geoNear": {
                    "near": point.model_dump(),
                    "distanceField": "distance",
                }
            }
        ],
        projection_model=ShopWithDistance,
    ).to_list(n)
