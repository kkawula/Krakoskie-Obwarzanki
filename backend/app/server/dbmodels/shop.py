from typing import List

from beanie import Document, Insert, before_event
from pydantic import BaseModel, ConfigDict

from .seller import Seller
from .user import PrivateUser as User
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

    @before_event(Insert)
    def capitalize_name(self):
        raise Exception("testowe")
        print("HHHHHHHHHHHHHHHHH")
        self.opening_time = self.opening_time.strftime("%H:%M")
        self.closing_time = self.closing_time.strftime("%H:%M")


class ShopByCommunity(Document, baseShop):
    confirmed_by: List[User]
    notes: List[str]

    class Settings:
        name = "shops_by_community"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]
