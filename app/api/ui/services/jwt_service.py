import datetime as dt
from typing import Annotated, Any, Dict

from fastapi import Depends
from app.api.ui.models.auth_model import TokenData, TokenResponse
from app.core.config import jwt_settings

import jwt


class JwtService:
    def verify_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                key=jwt_settings.SECRET_KEY,
                algorithms=[jwt_settings.ALGORITHM],
            )

            return TokenData(**payload)
        except jwt.PyJWTError as _e:
            return None

    def generate_access_token(
        self, data: Dict[Any, Any], expires_delta: dt.timedelta | None = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = dt.datetime.now(dt.timezone.utc) + expires_delta
        else:
            expire = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
                minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire, "nbf": dt.datetime.now(dt.timezone.utc)})

        token = jwt.encode(
            to_encode, key=jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM
        )

        return TokenResponse(
            access_token=token,
            token_type="bearer",
        )


def get_jwt_service():
    return JwtService()


CommonJwtService = Annotated[JwtService, Depends(get_jwt_service, use_cache=True)]


def jwt_verify(
    token: str,
    jwt_service: CommonJwtService,
) -> TokenData | None:
    return jwt_service.verify_token(token=token)


CommonJwtVerify = Annotated[
    TokenData | None,
    Depends(jwt_verify),
]
