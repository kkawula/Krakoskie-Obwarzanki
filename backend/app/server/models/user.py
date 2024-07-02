from beanie import Document
from pydantic import BaseModel


class User(Document):
    username: str
    hashed_password: str
    email: str | None = None
    full_name: str | None = None

    class Settings:
        name = "users"

    @staticmethod
    async def get_user(username: str | None = None, user_id: str | None = None):
        if username:
            return await User.find_one(User.username == username)

        if user_id:
            return await User.get(user_id)

        return None


class UserData(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
