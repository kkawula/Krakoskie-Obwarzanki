import logging
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, Security, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from .auth.auth import (
    authenticate_user,
    get_current_user,
    get_new_access_token,
    get_new_refresh_token,
    get_password_hash,
    refresh_token,
)
from .auth.jwt_encoder import JWTEncoder
from .auth.token import Token, TokenResponse
from .database import init_db
from .dbmodels.seller import Seller
from .dbmodels.shop import Shop, ShopQuery
from .dbmodels.user import PublicUser, User, UserInput
from .dbmodels.util_types import Point
from .outputmodels.shop import ShopWithDistance, ShopWithPosition


@asynccontextmanager
async def lifespan(_app: FastAPI):
    load_dotenv()
    await init_db()
    await JWTEncoder.load_security_details()
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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Logs which fields caused the validation error and returns a 422 response
    """
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


@app.get("/", tags=["Root"])
async def root():
    return RedirectResponse(url="/docs")


@app.get("/shops", tags=["Shops"], response_model=list[ShopWithPosition])
async def all_shops():
    shops = await Shop.all().to_list()
    return shops


@app.post("/shops/create", tags=["Shops"], response_model=ShopWithPosition)
async def create_shop(
    shop: ShopWithPosition,
    current_user: Annotated[
        User, Security(get_current_user, scopes=["access", "seller"])
    ],
):
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


async def create_user(query: UserInput):
    username = query.username.lower()
    existing_user = await User.get_user(username=username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    if query.email:
        email = query.email.lower()
        existing_user = await User.get_user(email=email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    hashed_password = get_password_hash(query.password)

    try:
        user = User(
            username=username,
            hashed_password=hashed_password,
            email=email,
            full_name=query.name,
            scopes=["user:full"],
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    return user


@app.post("/user/register", tags=["User"], response_model=PublicUser)
async def register_user(user: Annotated[User, Depends(create_user)]):
    await user.insert()
    return PublicUser(**user.model_dump())


@app.post("/user/register_seller", tags=["Seller"], response_model=PublicUser)
async def register_seller(user: Annotated[User, Depends(create_user)]):
    if not user.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seller must provide an email",
        )

    if not user.full_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seller must provide a full name",
        )

    user.scopes.append("seller")
    await user.insert()

    seller = Seller(user=user)

    try:
        await seller.insert()
    except Exception:
        await user.delete()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seller could not be created",
        )
    return PublicUser(**user.model_dump())


@app.post("/user/login", tags=["User"], response_model=TokenResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    login = form_data.username.lower()
    user, error_msg = await authenticate_user(login, form_data.password)
    if error_msg:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error_msg)

    access_token = get_new_access_token(user, scopes=form_data.scopes + user.scopes)
    refresh_token = get_new_refresh_token(user, scopes=form_data.scopes + user.scopes)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@app.post("/user/refresh", tags=["User"], response_model=Token)
async def refresh_access_token(
    refresh_token: Annotated[str, Security(refresh_token, scopes=["refresh"])],
):
    return refresh_token


@app.get("/user/me/", tags=["User"], response_model=PublicUser)
async def read_users_me(
    current_user: Annotated[User, Security(get_current_user, scopes=["access"])],
):
    return current_user
