from typing import Tuple

from pydantic import BaseModel, model_validator
from typing_extensions import Literal


class Point(BaseModel):
    # type is needed to be able to use 2d-sphere index in MongoDB
    type: Literal["Point"] = "Point"
    coordinates: Tuple[float, float]

    @model_validator(mode="before")
    def set_coordinates(cls, values):
        lng = values.get("lng")
        lat = values.get("lat")
        if lng and lat:
            values["coordinates"] = [lng, lat]
        return values
