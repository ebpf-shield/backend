from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from app.api.ui.models.auth_model import StateAuth
from app.api.ui.services.jwt_service import (
    CommonJwtService,
    JwtService,
    get_jwt_service,
)

# We use a depracted flow in OAuth2 because it's not a real project.
# We should switch an OAuth2 provider
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./api/ui/auth/token")


# This is a bigger lie and we should absolutely use a real OAuth2 provider
# It's not a really a lie it's just plain JWT authentication which does not support advanced authorization machinism
class JWTBearerDeps(HTTPBearer):
    _jwt_service: JwtService

    def __init__(
        self,
        jwt_service: CommonJwtService,
        auto_error: bool = True,
    ):
        self._jwt_service = jwt_service
        super(JWTBearerDeps, self).__init__(
            auto_error=auto_error, description="Jwt Bearer"
        )

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearerDeps, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self.is_valid_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            request.auth = credentials
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def is_valid_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = self._jwt_service.verify_token(jwtoken)
        except Exception as _e:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid


def get_jwt_bearer(
    jwt_service: CommonJwtService = Depends(get_jwt_service, use_cache=True),
) -> JWTBearerDeps:
    return JWTBearerDeps(jwt_service=jwt_service, auto_error=True)


CommonJWTBearerDeps = Annotated[
    JWTBearerDeps,
    Depends(get_jwt_bearer, use_cache=True),
]

invalid_or_expired_token = HTTPException(
    status_code=403,
    detail="Invalid token or expired token.",
    headers={"WWW-Authenticate": "Bearer"},
)


class JWTBearer(HTTPBearer):
    _jwt_service: JwtService

    def __init__(
        self,
        auto_error: bool = True,
    ):
        self._jwt_service = JwtService()
        super(JWTBearer, self).__init__(auto_error=auto_error, description="Jwt Bearer")

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )

            try:
                payload = self._jwt_service.verify_token(credentials.credentials)
            except Exception as _e:
                raise invalid_or_expired_token

            if not payload:
                raise invalid_or_expired_token

            request.state.auth = {
                "token": credentials.credentials,
                "payload": payload,
            }

            return credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


def get_auth_state(request: Request):
    auth = request.state.auth
    if not auth:
        raise HTTPException(
            status_code=403,
            detail="Invalid token or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return StateAuth(**request.state.auth)


CommonRequestStateAuth = Annotated[
    StateAuth,
    Depends(get_auth_state),
]
