from datetime import time
from typing import List, Tuple

from beanie import Document

from .review import Review
from .user import PrivateUser as User
from .util_types import Point


class Seller(Document):
    reviews: List[Review]
    availability_hours: List[Tuple[time, time]]
    most_common_spots: List[Point]
    user: User
