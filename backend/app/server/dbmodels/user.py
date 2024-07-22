from typing import List

from beanie import Document
from pydantic import BaseModel, ConfigDict, EmailStr


class User(Document):
    username: str
    hashed_password: str
    email: EmailStr | None = None
    full_name: str | None = None
    scopes: List[str] = []

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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "test",
                "password": "test",
                "email": "example@email.com",
                "full_name": "Test User",
            }
        }
    )


class PublicUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
