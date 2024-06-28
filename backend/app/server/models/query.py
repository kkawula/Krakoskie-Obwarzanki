from pydantic import BaseModel


class Query:
    class ShopLocation(BaseModel):
        lat: float
        lng: float

    class ShopsByDistance(ShopLocation):
        radius: float

        class Config:
            json_schema_extra = {
                "example": {
                    "lat": 50.086776271666000,
                    "lng": 19.915122985839847,
                    "radius": 1000,
                }
            }

    class ShopsByNumber(ShopLocation):
        n_closest: int

        class Config:
            json_schema_extra = {
                "example": {
                    "lat": 50.086776271666000,
                    "lng": 19.915122985839847,
                    "n_closest": 5,
                }
            }

    class UserRegister(BaseModel):
        username: str
        password: str

        class Config:
            json_schema_extra = {
                "example": {"username": "user", "password": "password"}
            }
