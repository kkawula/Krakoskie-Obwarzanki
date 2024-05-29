from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from server.database import init
from server.models.shop import Shop

app = FastAPI()


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


# @app.get("/shops/by_distance", tags=["Shops"])
# async def get_shops_by_dist(query: ShopsByDistance):
#     r = query.r
#     lat = query.lat
#     long = query.long
#     shops = await Shop.filter_by_distance(
#         localization=(lat, long), radius=r).to_list()
#     return shops
