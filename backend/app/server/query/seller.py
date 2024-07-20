from pydantic import BaseModel, ConfigDict


class SellerQuery:
    class SellerRegister(BaseModel):
        name: str
        surname: str
        username: str
        password: str
        email: str | None = None
        model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "name": "Test",
                    "surname": "Seller",
                    "username": "seller",
                    "password": "password",
                    "email": "example.seller@mail.com",
                }
            }
        )
