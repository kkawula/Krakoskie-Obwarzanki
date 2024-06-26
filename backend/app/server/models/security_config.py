import os

import jwt
from dotenv import load_dotenv


class SecurityConfig:
    SECRET_KEY = None
    ALGORITHM = None
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    def __new__(cls):
        raise TypeError("SecurityConfig is a static class and cannot be instantiated")

    def encode(to_encode):
        return jwt.encode(
            to_encode, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM
        )

    def decode(token):
        return jwt.decode(
            token, SecurityConfig.SECRET_KEY, algorithms=SecurityConfig.ALGORITHM
        )


async def load_security_details():
    load_dotenv()

    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        raise ValueError("You must set the SECRET_KEY environment variable")
    SecurityConfig.SECRET_KEY = secret_key

    algorithm = os.getenv("ALGORITHM")
    if not algorithm:
        raise ValueError("You must set the ALGORITHM environment variable")
    SecurityConfig.ALGORITHM = algorithm

    access_token_expire_str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    if not access_token_expire_str:
        raise ValueError(
            "You must set the ACCESS_TOKEN_EXPIRE_MINUTES environment variable"
        )
    SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expire_str)
