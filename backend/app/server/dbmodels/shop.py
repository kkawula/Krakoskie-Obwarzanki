from beanie import Document
from pydantic import BaseModel, ConfigDict, Field, conlist

from .seller import Seller
from .util_types import Point


class baseShop(BaseModel):
    location: Point
    flavors: conlist(item_type=str, max_length=32)
    price: float = Field(ge=0)
    card_payment: bool

    def __init__(self, *a, **kw):
        if not kw.get("location"):
            kw["location"] = Point(**kw)
        super().__init__(*a, **kw)


class Shop(Document, baseShop):
    owner: Seller | None = None
    opening_time: str = Field(pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")
    closing_time: str = Field(pattern=r"^([01]?[0-9]|2[0-3]):[0-5][0-9]$")

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


class ShopQuery:
    class ShopLocation(BaseModel):
        lat: float = Field(ge=-90, le=90)
        lng: float = Field(ge=-180, le=180)

    class ShopsByDistance(ShopLocation):
        radius: float = Field(ge=0)
        model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "lat": 50.086776271666000,
                    "lng": 19.915122985839847,
                    "radius": 1000,
                }
            }
        )

    class ShopsByNumber(ShopLocation):
        n_closest: int = Field(ge=1)
        model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "lat": 50.086776271666000,
                    "lng": 19.915122985839847,
                    "n_closest": 5,
                }
            }
        )
