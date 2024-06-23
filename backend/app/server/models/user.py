from beanie import Document


class User(Document):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

    class Settings:
        name = "users"
