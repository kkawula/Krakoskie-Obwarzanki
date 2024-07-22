from pydantic import BaseModel, ConfigDict, EmailStr


class UserQuery:
    class UserRegister(BaseModel):
        username: str
        password: str
        email: EmailStr | None = None
        name: str | None = None
        surname: str | None = None
        model_config = ConfigDict(
            json_schema_extra={
                "example": {
                    "username": "user",
                    "password": "password",
                    "email": "example@email.com",
                    "name": "Test User",
                }
            }
        )
