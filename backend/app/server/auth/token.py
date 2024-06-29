from pydantic import BaseModel


class Token(BaseModel):
    token_value: str


class TokenData(BaseModel):
    user_id: str | None = None
    type: str | None = None

    def __init__(self, payload):
        super().__init__(user_id=payload.get("sub"), type=payload.get("type"))


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
