from typing import List
from pydantic import root_validator
from beanie import Document

from server.models.utils import Point


class Shop(Document):
    owner_id: str = ""
    name: str
    location: Point
    flavors: List[str] = []
    card_payment: bool = False
    is_open_today: bool = True
    start_time: str
    end_time: str

    @root_validator(pre=True)
    def set_location(cls, values):
        if not values.get("location"):
            values["location"] = Point(**values)
        return values

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
                    "coordinates": [50.086776271666096, 19.915122985839847],
                },
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
            }
        }


class ShopWithPosition(Shop):
    lat: float
    lng: float

    @root_validator(pre=True)
    def set_location(cls, values):
        """
        Sets the latitude and longitude values based on the location coordinates, when the model is created.

        Args:
            values (dict): The input values for the model.

        Returns:
            dict: The updated values with latitude and longitude set.
        """
        location = values.get("location")
        if location:
            values["lng"] = location["coordinates"][0]
            values["lat"] = location["coordinates"][1]
        return values


class ShopWithDistance(ShopWithPosition):
    distance: float
