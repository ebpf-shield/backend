from typing import Annotated

import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.errors.invalid_password_exception import InvalidPasswordException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.models.user_model import User, UserLogin, UserRegister
from app.api.repositories.user_repository import CommonUserRepository, UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class AuthService:
    _user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def register_user(self, resisted_user: UserRegister):
        existing_user = await self._user_repository.get_by_email(resisted_user.email)
        if existing_user:
            raise EmailAlreadyExistsException()

        hashed_password = bcrypt.hashpw(
            resisted_user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        user_to_create = User(
            **resisted_user.model_copy(update={"password": hashed_password}).model_dump(
                by_alias=True
            )
        )
        return await self._user_repository.create(user=user_to_create)

    async def login_user(self, user_to_login: UserLogin):
        user = await self._user_repository.get_by_email(user_to_login.email)
        if not user:
            raise NoUserWithEmailException

        verify_password = bcrypt.checkpw(
            user_to_login.password.encode("utf-8"), user.password.encode("utf-8")
        )

        if not verify_password:
            raise InvalidPasswordException

        return user


def get_auth_service(user_repository: CommonUserRepository):
    return AuthService(user_repository=user_repository)


CommonAuthService = Annotated[AuthService, Depends(get_auth_service, use_cache=True)]
