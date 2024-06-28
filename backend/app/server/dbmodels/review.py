from beanie import Document

from .seller import Seller
from .user import PrivateUser as User


class Review(Document):
    rating: int
    review: str
    reviewer: User
    seller: Seller
