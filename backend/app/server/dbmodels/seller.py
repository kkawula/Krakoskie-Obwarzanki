from datetime import time
from typing import Tuple

from beanie import Document
from pydantic import conlist

from .review import Review
from .user import User
from .util_types import Point


class Seller(Document):
    reviews: conlist(Review) = []
    availability_days: conlist(
        item_type=str, max_length=7
    ) = []  # List of days of the week
    availability_hours: conlist(item_type=Tuple[time, time], max_length=7) = []
    most_common_spots: conlist(Point) = []
    user: User

    class Settings:
        name = "sellers"
        indexes = [
            [("most_common_spots", "2dsphere")],  # GEO index
        ]
