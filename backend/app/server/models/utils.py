from typing import Tuple

from pydantic import BaseModel, model_validator
from typing_extensions import Literal


class Point(BaseModel):
    type: str = Literal["Point"]
    coordinates: Tuple[float, float]

    @model_validator(mode="before")
    def set_coordinates(cls, values):
        longitude = values.get("lng")
        latitude = values.get("lat")
        if longitude and latitude:
            values["coordinates"] = [longitude, latitude]
        return values
