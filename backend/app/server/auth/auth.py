from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext

from ..dbmodels.user import PublicUser, User
from ..dbmodels.util_types import Result
from .jwt_encoder import JWTEncoder
from .token import Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
    scopes={
        "access": "Access token.",
        "refresh": "Refresh token.",
        "user:full": "Basic permissions for logged-in user.",
        "user:restrained": "Restrained user cannot add reviews and community shops.",
        "seller": "Basic permissions for the seller.",
    },
)


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


def get_new_refresh_token(user: User, scopes: list[str] = []):
    scopes = scopes.copy()
    scopes.append("refresh")
    return JWTEncoder.create_refresh_token(
        to_encode={"sub": str(user.id), "scopes": scopes}
    )


def get_new_access_token(user: User, scopes: list[str] = []):
    scopes = scopes.copy()
    scopes.append("access")
    return JWTEncoder.create_access_token(
        to_encode={"sub": str(user.id), "scopes": scopes}
    )


async def refresh_token(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
) -> Token:
    token_data = JWTEncoder.validate(token)
    JWTEncoder.check_sufficient_scopes(token_data, security_scopes.scopes)
    user = await obtain_user(token_data.user_id)
    return get_new_access_token(user, token_data.scopes)


async def get_current_user(
    security_scopes: SecurityScopes, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    token_data = JWTEncoder.validate(token)
    JWTEncoder.check_sufficient_scopes(token_data, security_scopes.scopes)
    user = await obtain_user(token_data.user_id)
    return PublicUser(**user.model_dump())
