from beanie import Document
from pydantic import BaseModel


class User(Document):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None

    class Settings:
        name = "users"


class UserData(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
