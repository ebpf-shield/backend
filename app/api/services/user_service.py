from typing import Annotated

from fastapi import Depends
from app.api.repositories.users_repository import CommonUserRepository, UserRepository


class UserService:
    user_repository: UserRepository

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository


def get_user_service(user_repository: CommonUserRepository):
    return UserService(user_repository=user_repository)


CommonUserService = Annotated[UserService, Depends(get_user_service, use_cache=True)]
