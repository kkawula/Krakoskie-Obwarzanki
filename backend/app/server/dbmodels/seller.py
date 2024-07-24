from datetime import time
from typing import List, Tuple

from beanie import Document
from pydantic import Field

from .review import Review
from .user import User
from .util_types import Point


class Seller(Document):
    reviews: List[Review] = Field(default_factory=list)
    availability_days: List[str] = Field(
        default_factory=list, max_length=7
    )  # List of days of the week
    availability_hours: List[Tuple[time, time]] = Field(
        default_factory=list, max_length=7
    )
    most_common_spots: List[Point] = Field(default_factory=list)
    user: User

    class Settings:
        name = "sellers"
        indexes = [
            [("most_common_spots", "2dsphere")],  # GEO index
        ]
