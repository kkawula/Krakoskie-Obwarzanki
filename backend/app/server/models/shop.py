from datetime import datetime, timedelta
from server.utils.distance import distance
from beanie import Document
from pydantic import BaseModel


class Shop(Document):
    owner_id: str = ""
    name: str
    longitude: float
    latitude: float
    flavors: list[str] = []
    card_payment: bool = False
    is_open_today: bool = True
    start_time: str
    end_time: str

    class Settings:
        name = "shops"

    class Config:
        schema_extra = {
            "example": {
                "name": "Pretzel Shop",
                "longitude": 19.915122985839847,
                "latitude": 50.086776271666096,
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
            }
        }

    def filter_by_distance(self, localization: tuple[float, float], radius: float) -> list["Shop"]:
        return self.all(limit=5).to_list()
        pass

    def filter_n_nearest(self, localization: tuple[float, float], n: int) -> list["Shop"]:
        pass


class ShopsByDistance(BaseModel):
    lat: float
    long: float
    r: float

    class Config:
        schema_extra = {
            "example": {
                "lat": 123.456,
                "long": 123.456,
                "r": 5,
            }
        }


class ShopsByNumber(BaseModel):
    n: int
    lat: float
    long: float

    class Config:
        schema_extra = {
            "example": {
                "lat": 123.456,
                "long": 123.456,
                "n": 5,
            }
        }
