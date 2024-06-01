from typing import Tuple
from pydantic import BaseModel, Field, root_validator


class Point(BaseModel):
    type: str = Field("Point", const=True)
    coordinates: Tuple[float, float]

    @root_validator(pre=True)
    def set_coordinates(cls, values):
        longitude = values.get('lng')
        latitude = values.get('lat')
        if longitude and latitude:
            values['coordinates'] = [longitude, latitude]
        return values
