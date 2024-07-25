from typing import List

from beanie import Document
from pydantic import BaseModel

from .shop import baseShop
from .user import User


class Confirmation(BaseModel):
    # User who confirmed the shop (can be anonymous)
    author: User | None = None
    confirmed_existing: bool
    note: str = ""


class ShopByCommunity(Document, baseShop):
    added_by: User
    initial_note: str = ""
    confirmations: List[Confirmation]

    class Settings:
        name = "shops_by_community"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]
