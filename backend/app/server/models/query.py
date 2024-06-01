from pydantic import BaseModel


class Query:
    class ShopLocation(BaseModel):
        lat: float
        long: float

    class ShopsByDistanceQuery(ShopLocation):
        r: float

        class Config:
            schema_extra = {
                "example": {
                    "lat": 50.086776271666000,
                    "long": 19.915122985839847,
                    "r": 5000,
                }
            }

    class ShopsByNumber(ShopLocation):
        n: int

        class Config:
            schema_extra = {
                "example": {
                    "lat": 50.086776271666096,
                    "long": 19.915122985839847,
                    "n": 5,
                }
            }
