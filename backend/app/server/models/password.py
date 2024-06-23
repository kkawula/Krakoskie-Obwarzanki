from beanie import Document, PydanticObjectId


class Password(Document):
    user_id: PydanticObjectId
    hashed_password: str

    class Settings:
        name = "passwords"
