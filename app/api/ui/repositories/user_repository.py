from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from pydantic import BaseModel, Field

from app.api.ui.models.user_model import User, UserDocument


class UIUserRepository:
    async def get_by_email(self, email: str):
        # TODO? Move this class?
        class GetUser(BaseModel):
            id: PydanticObjectId = Field(alias="_id")
            email: str
            name: str

        return await UserDocument.find_one({"email": email}).project(GetUser)

    async def get_by_id(self, user_id: PydanticObjectId) -> None:
        return await UserDocument.get(user_id)

    async def create(self, user: User):
        user_to_insert = UserDocument(**user.model_dump(by_alias=True))
        return await user_to_insert.insert()


def get_user_repository():
    return UIUserRepository()


UICommonUserRepository = Annotated[
    UIUserRepository, Depends(get_user_repository, use_cache=True)
]
