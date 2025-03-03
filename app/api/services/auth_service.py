from typing import Annotated, Any, Dict, Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.models.user_model import User, UserRegister
from app.api.repositories.user_repository import CommonUserRepository, UserRepository
from app.core.config import jwt_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    _user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register_user(self, resisted_user: UserRegister):
        existing_user = await self._user_repository.find_user_by_email(
            resisted_user.email
        )
        if existing_user:
            raise EmailAlreadyExistsException()

        hashed_password = bcrypt.hashpw(
            resisted_user.password.encode("utf-8"), bcrypt.gensalt()
        )

        user_to_create = User(
            **resisted_user.model_copy(
                update={"password": str(hashed_password)}
            ).model_dump(by_alias=True)
        )
        return await self._user_repository.create(user=user_to_create)

    # async def authenticate_user(
    #     self, email: str, password: str
    # ) -> Optional[Dict[str, str]]:
    #     user: Optional[Dict[str, str]] = fake_users_db.get(email)
    #     if not user or user["password"] != password:
    #         return None
    #     return user

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
