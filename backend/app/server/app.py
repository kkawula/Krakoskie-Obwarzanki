from contextlib import asynccontextmanager
from datetime import timedelta
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from server.database import init_db
from server.models.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_password_hash,
)
from server.models.password import Password
from server.models.query import Query
from server.models.shop import Shop, ShopWithDistance, ShopWithPosition
from server.models.token import Token
from server.models.user import User
from server.models.utils import Point


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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


@app.post("/users/register", tags=["User"], response_model=User)
async def register_user(query: Query.UserRegister):
    existing_user = await User.find_one(User.username == query.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    user_data = {
        "username": query.username,
    }
    user = User(**user_data)
    user_dict = await user.insert()

    await new_password(user_dict.id, query.password)

    return user


async def new_password(user_id: PydanticObjectId, password: str):
    hashed_password = get_password_hash(password)
    existing_password = await Password.find_one(Password.user_id == user_id)
    if existing_password:
        # If a password entry exists, update the hashed_password
        await existing_password.update({"$set": {"hashed_password": hashed_password}})
    else:
        # If no entry exists, insert a new password
        password_data = {
            "user_id": user_id,
            "hashed_password": hashed_password,
        }
        password = Password(**password_data)
        await password.insert()


@app.post("/token", tags=["User"])
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", tags=["Auth"], response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
