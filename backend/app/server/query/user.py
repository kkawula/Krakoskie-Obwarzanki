from pydantic import BaseModel, ConfigDict


class UserQuery:
    class UserRegister(BaseModel):
        username: str
        password: str
        model_config = ConfigDict(
            json_schema_extra={"example": {"username": "user", "password": "password"}}
        )
