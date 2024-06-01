from fastapi import APIRouter
from fastapi import HTTPException
from models.queries import *
from models.shop import Shop
from models.user import User
from schema.schemas import Repository


router = APIRouter()

repo = Repository()


@router.get("/")
async def get_all_shops():
    return repo.get_all_shops()


@router.post("/")
async def post_shop(shop: Shop):
    repo.shops.insert_one(dict(shop))


@router.post("/shops/by_distance")
async def get_shops_by_dist(query: ShopsByDistance):
    r = query.r
    lat = query.lat
    long = query.long
    shops = repo.filter_by_distance(
        repo.get_all_shops(), localization=(lat, long), radius=r
    )
    return shops


@router.post("/shops/by_number")
async def get_n_nearest_shops(query: ShopsByNumber):
    n = query.n
    lat = query.lat
    long = query.long
    shops = repo.filter_n_nearest(repo.get_all_shops(), localization=(lat, long), n=n)
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
    users.insert_one(user_doc)


@router.post("/login")
async def login(user: User):
    stored_user = users_collection.find_one({"username": user.username})
    if not stored_user or stored_user["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}


@router.get("/user/{username}")
async def get_user(username: str):
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
