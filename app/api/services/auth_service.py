from datetime import datetime, timedelta, timezone
from re import L
from typing import Annotated, Dict, Any, Optional
import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.repositories.users_repository import CommonUserRepository, UserRepository
from app.core.config import jwt_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(
        self, email: str, password: str
    ) -> Optional[Dict[str, str]]:
        user: Optional[Dict[str, str]] = fake_users_db.get(email)
        if not user or user["password"] != password:
            return None
        return user

    def create_access_token(self, data: Dict[str, Any]) -> str:
        expire: datetime = datetime.now(timezone.utc) + timedelta(
            minutes=jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode: Dict[str, Any] = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode, jwt_settings.SECRET_KEY, algorithm=jwt_settings.ALGORITHM
        )

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> str:
        try:
            payload = jwt.decode(
                token, jwt_settings.SECRET_KEY, algorithms=[jwt_settings.ALGORITHM]
            )

            email: Optional[str] = payload.get("sub")
            if email is None:
                raise HTTPException(status_code=401, detail="Invalid token")
            return email
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")


def get_auth_service(user_repository: CommonUserRepository):
    return AuthService(user_repository=user_repository)


CommonAuthService = Annotated[AuthService, Depends(get_auth_service, use_cache=True)]
