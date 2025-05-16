from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from pydantic import BaseModel, Field

from app.api.ui.models.user_model import UserDocument


class UIUserRepository:
    async def get_by_email(self, email: str):
        # TODO? Move this class?
        class GetUser(BaseModel):
            id: PydanticObjectId = Field(alias="_id")
            email: str
            name: str

        return await UserDocument.find_one({"email": email}).project(GetUser)


def get_user_repository():
    return UIUserRepository()


UICommonUserRepository = Annotated[
    UIUserRepository, Depends(get_user_repository, use_cache=True)
]
