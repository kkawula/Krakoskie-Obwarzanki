from pydantic import BaseModel

Token = str


class TokenData(BaseModel):
    user_id: str | None = None
    scopes: list[str] = []

    def __init__(self, payload):
        super().__init__(user_id=payload.get("sub"), scopes=payload.get("scopes", []))


class TokenResponse(BaseModel):
    access_token: Token
    refresh_token: Token
