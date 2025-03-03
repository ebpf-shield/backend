import datetime
from typing import Annotated, Any, Dict

from fastapi import Depends
from app.core.config import jwt_settings

import jwt


class JwtService:
    async def decode(self):
        pass

    async def generate_token(self, data: Dict[Any, Any]) -> str:
        expire = datetime.datetime.now() + datetime.timedelta(
            minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        data.update({"exp": expire, "nbf": datetime.now()})

        return jwt.encode(
            data, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM
        )

    async def verify(token: str) -> Dict[Any, Any] | None:
        try:
            return jwt.decode(
                token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM]
            )
        except jwt.PyJWTError:
            return None


def get_jwt_service():
    return JwtService()


CommonJwtService = Annotated[JwtService, Depends(get_jwt_service, use_cache=True)]
