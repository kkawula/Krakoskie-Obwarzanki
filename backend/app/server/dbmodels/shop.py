from typing import List

from beanie import Document
from pydantic import BaseModel, ConfigDict

from .seller import Seller
from .user import User
from .util_types import Point


class baseShop(BaseModel):
    location: Point
    flavors: List[str]
    price: float
    card_payment: bool

    def __init__(self, *a, **kw):
        if not kw.get("location"):
            kw["location"] = Point(**kw)
        super().__init__(*a, **kw)


class Shop(Document, baseShop):
    owner: Seller | None = None
    opening_time: str
    closing_time: str

    class Settings:
        name = "shops"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "location": {
                    "type": "Point",
                    "coordinates": [50.086776271666096, 19.915122985839847],
                },
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
            }
        }
    )


class ShopByCommunity(Document, baseShop):
    confirmed_by: List[User]
    notes: List[str]

    class Settings:
        name = "shops_by_community"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]
