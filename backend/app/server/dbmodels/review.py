from beanie import Document, PydanticObjectId
from pydantic import ConfigDict, Field

from .user import User


class Review(Document):
    rating: int = Field(ge=1, le=5)
    review: str = ""
    reviewer: User | None = None
    seller_id: PydanticObjectId

    class Settings:
        name = "reviews"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "rating": 5,
                "review": "Great seller",
                "seller_id": "5f4a3b2f9e6f3b3b3f3b3f3b",
            }
        }
    )
