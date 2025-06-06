from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Token(BaseModel):
    access_token: str
    token_type: str


# It has to be str and not PydanticObjectId because it is used in JWT
class BasicTokenPayload(BaseModel):
    email: str
    id: str
    name: str


class MemeberTokenPayload(BasicTokenPayload):
    model_config = ConfigDict(
        validate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
    )

    organization_id: str = Field(alias="organizationId", description="Organization ID")


class BaseTokenData(BaseModel):
    exp: int = Field(description="Expiration time in seconds")
    nbf: int = Field(description="Not before time in seconds")


class BasicTokenData(BaseTokenData, BasicTokenPayload):
    pass


class MemberTokenData(BaseTokenData, MemeberTokenPayload):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"


class BasicStateAuth(BaseModel):
    token: str
    payload: BasicTokenData


class MemberStateAuth(BasicStateAuth):
    payload: MemberTokenData
