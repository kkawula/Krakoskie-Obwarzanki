from typing import Tuple

from pydantic import BaseModel, model_validator
from typing_extensions import Literal


class Point(BaseModel):
    # type is needed to be able to use 2dsphere index in MongoDB
    type: Literal["Point"] = "Point"
    coordinates: Tuple[float, float]

    @model_validator(mode="before")
    def set_coordinates(cls, values):
        lng = values.get("lng")
        lat = values.get("lat")
        if lng and lat:
            values["coordinates"] = [lng, lat]
        return values


# class TimeStringField(Field):
#     """
#     A custom field for handling datetime.time objects as strings in MongoDB.
#     """

#     def encode(self, value: bytes) -> bytes:
#         # Convert time object to a string
#         return value.strftime("%H:%M:%S")

#     def decode(self, value: bytes) -> time:
#         # Convert string back to a time object
#         return datetime.strptime(value, "%H:%M:%S").time()
