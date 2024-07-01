import os

import jwt
from fastapi import HTTPException, status
from jwt.exceptions import InvalidTokenError

from .token import TokenData


class SecurityConfig:
    SECRET_KEY = None
    ALGORITHM = None
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 30

    def __new__(cls):
        raise TypeError("SecurityConfig is a static class and cannot be instantiated")

    def encode(to_encode):
        return jwt.encode(
            to_encode, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM
        )

    def decode(token):
        try:
            payload = jwt.decode(
                token, SecurityConfig.SECRET_KEY, algorithms=SecurityConfig.ALGORITHM
            )
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token."
            )

        return TokenData(payload)

    def validate(token):
        token_data = SecurityConfig.decode(token)
        if token_data.user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User ID not found in token.",
            )
        if token_data.type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token type not found in token.",
            )

        return token_data


async def load_security_details():
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("You must set the SECRET_KEY environment variable")
    SecurityConfig.SECRET_KEY = secret_key

    algorithm = os.getenv("ALGORITHM")
    if not algorithm:
        raise ValueError("You must set the ALGORITHM environment variable")
    SecurityConfig.ALGORITHM = algorithm

    access_token_expire_str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if access_token_expire_str:
        SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_str)

    refresh_token_expire_str = os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")
    if refresh_token_expire_str:
        SecurityConfig.REFRESH_TOKEN_EXPIRE_DAYS = int(refresh_token_expire_str)
