from typing import Tuple
from pydantic import BaseModel, Field


class Point(BaseModel):
    type: str = Field("Point", const=True)
    coordinates: Tuple[float, float]
