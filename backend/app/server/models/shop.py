from datetime import datetime, timedelta

from beanie import Document


class Shop(Document):
    owner_id: str = ""
    name: str
    longitude: float
    latitude: float
    flavors: list[str] = []
    card_payment: bool = False
    is_active_today: bool = True
    startTime: datetime
    endTime: datetime

    class Settings:
        name = "shops"

    class Config:
        schema_extra = {
            "example": {
                "name": "Pretzel Shop",
                "longitude": 123.456,
                "latitude": 123.456,
                "flavors": ["cheese", "cinnamon"],
                "card_payment": True,
                "is_active_today": True,
                "startTime": datetime.now().isoformat(),
                "endTime": (datetime.now() + timedelta(hours=12)).isoformat(),
            }
        }
