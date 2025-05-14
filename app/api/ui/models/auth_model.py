from typing import Literal

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    email: str
    exp: int = Field(description="Expiration time in seconds")
    nbf: int = Field(description="Not before time in seconds")


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class StateAuth(BaseModel):
    token: str
    payload: TokenData
