from typing import List
from .user import User
from pydantic import BaseModel
from beanie import Document
from .shop import baseShop


class Confirmation(BaseModel):
    # User who confirmed the shop (can be anonymous)
    author: User | None = None
    confirmed_existing: bool
    note: str = ""


class ShopByCommunity(Document, baseShop):
    confirmed_by: List[User]
    initial_note: str
    confirmations: List[Confirmation]

    class Settings:
        name = "shops_by_community"
        indexes = [
            [("location", "2dsphere")],  # GEO index
        ]
