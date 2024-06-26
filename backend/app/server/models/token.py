from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None

    def __init__(self, payload):
        super().__init__(user_id=payload.get("sub"))
