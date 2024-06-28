from pydantic import BaseModel


class UserQuery:
    class UserRegister(BaseModel):
        username: str
        password: str

        class Config:
            json_schema_extra = {
                "example": {"username": "user", "password": "password"}
            }
