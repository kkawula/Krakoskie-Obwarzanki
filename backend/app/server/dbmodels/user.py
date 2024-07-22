from typing import List

from beanie import Document
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class User(Document):
    username: str = Field(min_length=4, max_length=32, pattern=r"^[a-zA-Z0-9]+$")
    hashed_password: str
    email: EmailStr | None = Field(default=None)
    full_name: str | None = Field(min_length=4, max_length=128, default=None)
    scopes: List[str] = Field(default_factory=list)

    @staticmethod
    async def get_user(
        username: str | None = None,
        email: str | None = None,
        user_id: str | None = None,
    ):
        if username:
            return await User.find_one(User.username == username)

        if email:
            return await User.find_one(User.email == email)

        if user_id:
            return await User.get(user_id)

        return None

    class Settings:
        name = "users"


class PublicUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None


class UserInput(BaseModel):
    username: str
    password: str
    email: EmailStr | None = None
    name: str | None = None
    surname: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "user",
                "password": "password",
                "email": "example@email.com",
                "name": "Test User",
            }
        }
    )
