from typing import Annotated

from fastapi import Depends

from app.api.ui.models.user_model import User, UserDocument


class UIAuthRepository:
    async def get_by_email(self, email: str):
        return await UserDocument.find_one({"email": email})

    async def create(self, user: User):
        user_to_insert = UserDocument(**user.model_dump(by_alias=True))
        return await user_to_insert.insert()


def get_auth_repository():
    return UIAuthRepository()


UICommonAuthRepository = Annotated[
    UIAuthRepository, Depends(get_auth_repository, use_cache=True)
]
