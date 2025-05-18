from typing import Annotated

import bcrypt
from fastapi import Depends

from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.errors.invalid_password_exception import InvalidPasswordException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.ui.models.user_model import User, UserLogin, UserRegister
from app.api.ui.repositories.auth_repository import (
    UIAuthRepository,
    UICommonAuthRepository,
)


class UIAuthService:
    _auth_repository: UIAuthRepository

    def __init__(self, auth_repository: UIAuthRepository):
        self._auth_repository = auth_repository

    async def register_user(self, resisted_user: UserRegister):
        existing_user = await self._auth_repository.get_by_email(resisted_user.email)
        if existing_user:
            raise EmailAlreadyExistsException()

        hashed_password = bcrypt.hashpw(
            bytes(resisted_user.password, encoding="utf-8"),
            bcrypt.gensalt(),
        )

        user_to_create = User(
            **resisted_user.model_copy(update={"password": hashed_password}).model_dump(
                by_alias=True
            )
        )
        return await self._auth_repository.create(user=user_to_create)

    async def login_user(self, user_to_login: UserLogin):
        user = await self._auth_repository.get_by_email(user_to_login.email)
        if not user:
            raise NoUserWithEmailException

        verify_password = bcrypt.checkpw(
            bytes(user_to_login.password, encoding="utf-8"),
            bytes(user.password, encoding="utf-8"),
        )

        if not verify_password:
            raise InvalidPasswordException

        return user


def get_auth_service(auth_repository: UICommonAuthRepository):
    return UIAuthService(auth_repository=auth_repository)


UICommonAuthService = Annotated[
    UIAuthService, Depends(get_auth_service, use_cache=True)
]
