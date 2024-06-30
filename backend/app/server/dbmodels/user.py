from beanie import Document
from pydantic import BaseModel, ConfigDict


class User(Document):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None

    class Settings:
        name = "users"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "test",
                "password": "test",
            }
        }
    )


class PublicUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
