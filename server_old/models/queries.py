from pydantic import BaseModel


class ShopsByDistance(BaseModel):
    r: float
    lat: float
    long: float


class ShopsByNumber(BaseModel):
    n: int
    lat: float
    long: float
