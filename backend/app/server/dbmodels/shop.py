from typing import List

from beanie import Document
from pydantic import BaseModel, ConfigDict

from .seller import Seller
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
                    "coordinates": [19.915122985839847, 50.086776271666096],
                },
                "flavors": ["Sezam", "Mak"],
                "price": 5.0,
                "card_payment": True,
                "opening_time": "08:00",
                "closing_time": "16:00",
            }
        }
    )
