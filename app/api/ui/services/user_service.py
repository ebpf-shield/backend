from typing import Annotated

from fastapi import Depends

from app.api.ui.repositories.user_repository import (
    UICommonUserRepository,
    UIUserRepository,
)


class UserService:
    _user_repository: UIUserRepository

    def __init__(self, user_repository: UIUserRepository):
        self._user_repository = user_repository

    async def get_user_by_email(self, email: str):
        return await self._user_repository.get_by_email(email)


def get_user_service(user_repository: UICommonUserRepository):
    return UserService(user_repository=user_repository)


CommonUserService = Annotated[UserService, Depends(get_user_service, use_cache=True)]
