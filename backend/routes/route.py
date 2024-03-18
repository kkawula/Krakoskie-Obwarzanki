from fastapi import APIRouter, HTTPException
from models.shop import Shop
from models.user import User
from models.query import *
from config.database import collection

from schema.schemas import list_serial, filter_by_distance, filter_n_nearest, get_all_data
from bson import ObjectId

router = APIRouter()


@router.get("/")
async def get_all_shops():
    shops = get_all_data(collection.find())
    return shops


@router.post("/")
async def post_shop(shop: Shop):
    print(shop)
    collection.insert_one(dict(shop))


@router.post("/shops/by_distance")
async def get_shops_by_dist(query: ShopsByDistance):
    r = query.r
    lat = query.lat
    long = query.long
    shops = filter_by_distance(
        collection.find(), localization=(lat, long), radius=r)
    return shops


@router.post("/shops/by_number")
async def get_n_nearest_shops(query: ShopsByNumber):
    n = query.n
    lat = query.lat
    long = query.long
    shops = filter_n_nearest(collection.find(), localization=(lat, long), n=n)
    return shops


# @router.post("/")
# async def create_account(user: User):
#     username_logins.insert_one(dict(user))

# @router.post("/login/")
# async def login(username: str, password: str):

@router.post("/register")
async def register(user: User):
    # Hash the password before storing it
    user_doc = {"username": user.username, "password": user.password}
    users_collection.insert_one(user_doc)


@router.post("/login")
async def login(user: User):
    stored_user = users_collection.find_one({"username": user.username})
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}


@router.get("/user/{username}")
async def get_user(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
