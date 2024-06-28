from typing import Optional

from beanie import Document, PydanticObjectId

from .user import User


class Review(Document):
    rating: int
    review: Optional[str]
    reviewer: Optional[User]
    seller_id: PydanticObjectId

    class Settings:
        name = "reviews"
