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
                    "coordinates": [50.086776271666096, 19.915122985839847]
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

    @root_validator(pre=True)
    def set_lat_long(cls, values):
        """
        Sets the latitude and longitude values based on the location coordinates, when the model is created.

        Args:
            values (dict): The input values for the model.

        Returns:
            dict: The updated values with latitude and longitude set.
        """
        location = values.get('location')
        if location:
            values['latitude'] = location['coordinates'][0]
            values['longitude'] = location['coordinates'][1]
        return values
