from datetime import time
from typing import List, Tuple

from beanie import Document

from .review import Review
from .user import User
from .util_types import Point


class Seller(Document):
    reviews: List[Review]
    availability_days: List[str]  # List of days of the week
    availability_hours: List[Tuple[time, time]]
    most_common_spots: List[Point]
    user: User

    class Settings:
        name = "sellers"
        indexes = [
            [("most_common_spots", "2dsphere")],  # GEO index
        ]
