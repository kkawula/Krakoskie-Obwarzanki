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

    def __init__(self, user: User):
        super().__init__(
            username=user.username, email=user.email, full_name=user.full_name
        )
