from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from server.database import init
from server.models.shop import Shop, ShopsByDistance

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


@app.get("/shops/by_distance", tags=["Shops"])
async def get_shops_by_dist(query: ShopsByDistance):
    r = query.r
    lat = query.lat
    long = query.long
    shops = await Shop.filter_by_distance(
        localization=(lat, long), radius=r).to_list()
    return shops


@app.get("/shops/by_number", tags=["Shops"])
async def get_n_nearest_shops(query: ShopsByDistance):
    n = query.n
    lat = query.lat
    long = query.long
    shops = await Shop.filter_n_nearest(
        localization=(lat, long), n=n).to_list()
    return shops
