from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)

from app.api.ui.models.auth_model import BasicStateAuth, MemberStateAuth
from app.api.ui.services.jwt_service import (
    JwtService,
)

# We use a depracted flow in OAuth2 because it's not a real project.
# We should switch an OAuth2 provider
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./api/ui/auth/token")


# This is a bigger lie and we should absolutely use a real OAuth2 provider
# It's not a really a lie it's just plain JWT authentication which does not support advanced authorization machinism


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
        raise invalid_or_expired_token

    state = BasicStateAuth(**request.state.auth)
    return state


CommonRequestStateAuth = Annotated[
    BasicStateAuth,
    Depends(get_auth_state),
]


# TODO? Can we find a better name
def get_auth_state_with_org(
    request: Request,
):
    auth = request.state.auth
    if not auth:
        raise invalid_or_expired_token

    if "organization_id" not in auth["payload"]:
        raise invalid_or_expired_token

    state = MemberStateAuth(**request.state.auth)

    return state


CommonRequestStateAuthWithOrg = Annotated[
    MemberStateAuth,
    Depends(get_auth_state_with_org),
]
