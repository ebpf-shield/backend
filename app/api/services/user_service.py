from typing import Annotated

from fastapi import Depends
from app.api.models.user_model import User
from app.api.repositories.user_repository import CommonUserRepository, UserRepository


class UserService:
    _user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def get_user_by_email(self, email: str):
        return await self._user_repository.get_by_email(email)

    async def create(self, user: User):
        return await self._user_repository.create(user)


def get_user_service(user_repository: CommonUserRepository):
    return UserService(user_repository=user_repository)


CommonUserService = Annotated[UserService, Depends(get_user_service, use_cache=True)]
