from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm

from .auth.auth import (
    authenticate_user,
    get_current_user,
    get_new_access_token,
    get_new_refresh_token,
    get_password_hash,
    get_user_by_username,
    refresh_token,
)
from .auth.security_config import SecurityConfig
from .auth.token import Token, TokenResponse
from .database import init_db
from .models.shop import Shop, ShopWithDistance, ShopWithPosition
from .models.user import User, UserData
from .models.util_types import Point
from .query.shop import ShopQuery
from .query.user import UserQuery


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_dotenv()
    await init_db()
    await SecurityConfig.load_security_details()
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
async def get_shops_by_dist(query: ShopQuery.ShopsByDistance):
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
async def get_n_nearest_shops(query: ShopQuery.ShopsByNumber):
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


@app.post("/user/register", tags=["User"], response_model=UserData)
async def register_user(query: UserQuery.UserRegister):
    existing_user = await get_user_by_username(query.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = get_password_hash(query.password)

    user = User(username=query.username, hashed_password=hashed_password)
    await user.insert()

    return UserData(**user.model_dump())


@app.post("/user/login", tags=["User"], response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    user, error_msg = await authenticate_user(form_data.username, form_data.password)
    if error_msg:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_msg,
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = get_new_access_token(user)
    refresh_token = get_new_refresh_token(user)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@app.post("/user/refresh", tags=["User"], response_model=Token)
async def refresh_access_token(
    refresh_token: Annotated[str, Depends(refresh_token)],
):
    return refresh_token


@app.get("/user/me/", tags=["User"], response_model=UserData)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
