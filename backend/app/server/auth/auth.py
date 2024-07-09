from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from ..dbmodels.user import PublicUser, User
from ..dbmodels.util_types import Result
from .jwt_encoder import JWTEncoder
from .token import Token, TokenType

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def obtain_user(user_id: str):
    user = await User.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )
    return user


async def authenticate_user(username: str, password: str) -> Result:
    user = await User.get_user(username=username)
    if not user:
        return None, "User not found."

    hashed_password = user.hashed_password
    if not hashed_password or not verify_password(password, hashed_password):
        return None, "Incorrect password."

    return user, None


def create_token(to_encode: dict, expires_delta: timedelta):
    if not expires_delta:
        raise ValueError("expires_delta must be a timedelta object.")

    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = JWTEncoder.encode(to_encode)

    return Token(encoded_jwt)


def get_new_access_token(user: User):
    access_token_expires = timedelta(minutes=JWTEncoder.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_token(
        to_encode={"sub": str(user.id), "type": "access"},
        expires_delta=access_token_expires,
    )


def get_new_refresh_token(user: User):
    refresh_token_expires = timedelta(days=JWTEncoder.REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(
        to_encode={"sub": str(user.id), "type": "refresh"},
        expires_delta=refresh_token_expires,
    )


async def refresh_token(refresh_token: str) -> Token:
    token_data = JWTEncoder.validate(refresh_token)

    if token_data.type != TokenType.REFRESH:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    user = await obtain_user(token_data.user_id)

    return get_new_access_token(user)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    token_data = JWTEncoder.validate(token)

    if token_data.type != TokenType.ACCESS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    user = await obtain_user(token_data.user_id)

    return PublicUser(**user.model_dump())
