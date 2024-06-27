from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from server.models.security_config import SecurityConfig
from server.models.token import Token, TokenData
from server.models.user import User, UserData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user_by_username(username: str):
    return await User.find_one(User.username == username)


async def authenticate_user(
    username: str, password: str
) -> tuple[Optional[User], Optional[str]]:
    user = await get_user_by_username(username)
    if not user:
        return None, "User not found."

    hashed_password = user.hashed_password
    if not hashed_password or not verify_password(password, hashed_password):
        return None, "Incorrect password."

    return user, None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = SecurityConfig.encode(to_encode)
    print(encoded_jwt)

    return Token(access_token=encoded_jwt)


def get_new_token(user: User):
    access_token_expires = timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    try:
        payload = SecurityConfig.decode(token)
        token_data = TokenData(payload)
        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token.",
            )

    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
        )
    user = await User.get(token_data.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return UserData(**user.model_dump())
