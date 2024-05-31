from typing import List
from typing import Optional

from beanie import Document
from pydantic import BaseModel
from pydantic import Field


class Point(BaseModel):
    type: str = Field("Point", const=True)
    coordinates: List[float]


class Shop(Document):
    owner_id: str = ""
    name: str
    location: Point
    flavors: List[str] = []
    card_payment: bool = False
    is_open_today: bool = True
    start_time: str
    end_time: str
    distance: Optional[float]

    class Settings:
        collection = "shops"

    class Config:
        schema_extra = {
            "example": {
                "name": "Pretzel Shop",
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


class ShopsByDistance(BaseModel):
    lat: float
    long: float
    r: float

    class Config:
        schema_extra = {
            "example": {
                "lat": 50.086776271666096,
                "long": 19.915122985839847,
                "r": 5,
            }
        }


class ShopsByNumber(BaseModel):
    lat: float
    long: float
    n: int

    class Config:
        schema_extra = {
            "example": {
                "lat": 50.086776271666096,
                "long": 19.915122985839847,
                "n": 5,
            }
        }
