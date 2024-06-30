from pydantic import ConfigDict, model_validator

from ..dbmodels.shop import Shop


class ShopWithPosition(Shop):
    lat: float
    lng: float

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        location = kw.get("location")
        if location:
            self.lat = location["coordinates"][1]
            self.lng = location["coordinates"][0]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Pretzel Shop",
                "flavors": ["Sezam", "Mak"],
                "card_payment": True,
                "is_open_today": True,
                "start_time": "08:00",
                "end_time": "16:00",
                "lat": 50.086776271666096,
                "lng": 19.915122985839847,
            }
        }
    )

    @model_validator(mode="before")
    def set_location(cls, values: Shop | dict):
        if type(values) == Shop:
            values = values.model_dump()

        if "lat" not in values and "lng" not in values:
            values["lat"] = values["location"]["coordinates"][1]
            values["lng"] = values["location"]["coordinates"][0]
        return values


class ShopWithDistance(ShopWithPosition):
    distance: float
