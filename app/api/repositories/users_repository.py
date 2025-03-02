from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.user_model import UserDocument


class UserRepository:
    async def find_user_by_email(self, email: str):
        return await UserDocument.find_one({"email": email})

    async def find_user_by_id(self, user_id: PydanticObjectId) -> None:
        raise NotImplementedError


def get_user_repository():
    return UserRepository()


CommonUserRepository = Annotated[
    UserRepository, Depends(get_user_repository, use_cache=True)
]
