from datetime import datetime, timedelta, timezone
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from server.models.security_config import SecurityConfig
from server.models.token import TokenData
from server.models.user import User, UserData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    return await User.find_one(User.username == username)


async def get_hashed_password(user_id: PydanticObjectId):
    user = await User.get(user_id)
    if not user:
        return None
    return user.hashed_password


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return None

    hashed_password = await get_hashed_password(user.id)

    if not hashed_password and not verify_password(password, hashed_password):
        return None

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = SecurityConfig.encode(to_encode)

    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = SecurityConfig.decode(token)
        token_data = TokenData(payload)
        if token_data.user_id is None:
            raise credentials_exception

    except InvalidTokenError:
        raise credentials_exception
    user = await User.get(token_data.user_id)
    if user is None:
        raise credentials_exception
    return UserData(user)


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user
