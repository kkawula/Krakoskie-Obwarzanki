from typing import List

from beanie import Document
from pydantic import model_validator
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

    def __init__(self, *a, **kw):
        if not kw.get("location"):
            # It the same as setting kw["location"] to
            #              = Point(type="Point", coordinates=[kw["lng"], kw["lat"]])
            kw["location"] = Point(**kw)
        super().__init__(*a, **kw)

    class Settings:
        name = "shops"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]

    class Config:
        json_schema_extra = {
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

    def __init__(self, *a, **kw):
        print("init with position")
        super().__init__(*a, **kw)
        location = kw.get("location")
        if location:
            self.lat = location["coordinates"][1]
            self.lng = location["coordinates"][0]

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Pretzel Shop",
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
                "lat": 50.086776271666096,
                "lng": 19.915122985839847,
            }
        }

    @model_validator(mode="before")
    def set_location(cls, values: Shop | dict):
        """
        Sets the latitude and longitude values based on the location coordinates,
          when the model is created.

        Args:
            values (dict): The input values for the model.

        Returns:
            dict: The updated values with latitude and longitude set.
        """
        if type(values) == Shop:
            values = values.model_dump()

        if "lat" not in values and "lng" not in values:
            values["lat"] = values["location"]["coordinates"][1]
            values["lng"] = values["location"]["coordinates"][0]
        return values


class ShopWithDistance(ShopWithPosition):
    distance: float
