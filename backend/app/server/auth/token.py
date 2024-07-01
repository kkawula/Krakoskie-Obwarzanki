from enum import Enum

from pydantic import BaseModel


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


Token = str


class TokenData(BaseModel):
    user_id: str | None = None
    type: TokenType | None = None

    def __init__(self, payload):
        super().__init__(
            user_id=payload.get("sub"), type=TokenType(payload.get("type"))
        )


class TokenResponse(BaseModel):
    access_token: Token
    refresh_token: Token
