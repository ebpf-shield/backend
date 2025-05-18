from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.errors.user_have_organization import UserHaveOrgException
from app.api.ui.models.user_model import GetUserDTO, UserDocument


class UIUserRepository:
    async def get_by_email(self, email: str):
        user = await UserDocument.find_one({"email": email}).project(GetUserDTO)

        if not user:
            raise NoUserWithEmailException

        return user

    async def get_by_id(self, user_id: PydanticObjectId):
        user = await UserDocument.find_one({"_id": user_id}).project(GetUserDTO)

        if not user:
            raise NoUserWithEmailException

        return user

    async def update_organization_by_user_id(
        self,
        organization_id: PydanticObjectId,
        user_id: PydanticObjectId,
        session: AsyncIOMotorClient = None,
    ):
        user = await UserDocument.find_one({"_id": user_id}, session=session)

        if not user:
            raise NoUserWithEmailException

        if user.organization_id:
            raise UserHaveOrgException

        user.organization_id = organization_id
        new_user = await user.save(session=session)

        return new_user


def get_user_repository():
    return UIUserRepository()


UICommonUserRepository = Annotated[
    UIUserRepository, Depends(get_user_repository, use_cache=True)
]
