from typing import List, Optional, Tuple
from enum import Enum
from pydantic import BaseModel,Field
from beanie import Document


class Point(BaseModel):
    type: str = Field("Point", const=True)
    coordinates: Tuple[float,float]

class Shop(Document):
    owner_id: str = ""
    name: str
    location: Point
    flavors: List[str] = []
    card_payment: bool = False
    is_open_today: bool = True
    start_time: str
    end_time: str

    class Settings:
        name = "shops"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]

    class Config:
        schema_extra = {
            "example": {
                "name": "Pretzel Shop",
                "location": {
                    "type": "Point",
                    "coordinates": [50.086776271666096,19.915122985839847]
                },
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
            }
        }

class ShopWithDistance(Shop):
    latitude: float
    longitude: float
    distance: float

class ShopsByDistance(BaseModel):
    lat: float
    long: float
    r: float

    class Config:
        schema_extra = {
            "example": {
                "lat": 50.086776271666096,
                "long": 19.915122985839847,
                "r": 5000,
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
                "long": 19.915122985839847   ,
                "n": 5,
            }
        }