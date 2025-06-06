from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.organization_model import CreateOrganizationDTO
from app.api.ui.repositories.organization_repository import (
    CommonUIOrganizationRepository,
    UIOrganizationRepository,
)
from app.api.ui.repositories.user_repository import (
    UICommonUserRepository,
    UIUserRepository,
)
from app.core.db import CommonDBClientManager, DBClientManager


class UIUserService:
    _user_repository: UIUserRepository
    _organization_repository: UIOrganizationRepository
    _db: DBClientManager

    def __init__(
        self,
        user_repository: UIUserRepository,
        organization_repository: UIOrganizationRepository,
        db: DBClientManager,
    ):
        self._user_repository = user_repository
        self._organization_repository = organization_repository
        self._db = db

    async def get_user_by_email(self, email: str):
        return await self._user_repository.get_by_email(email)

    async def get_user_by_id(self, user_id: PydanticObjectId):
        return await self._user_repository.get_by_id(user_id)

    async def create_organization_by_user_id(
        self, user_id: PydanticObjectId, organization: CreateOrganizationDTO
    ):
        # async with await self._process_repository._client.get_session() as session:
        session = await self._db.get_session()
        async with session.start_transaction():
            organization = await self._organization_repository.create(
                organization, session=session
            )

            user = await self._user_repository.update_organization_by_user_id(
                organization_id=organization.id, user_id=user_id, session=session
            )

            return user


def get_user_service(
    user_repository: UICommonUserRepository,
    organization_repository: CommonUIOrganizationRepository,
    db: CommonDBClientManager,
):
    return UIUserService(
        user_repository=user_repository,
        organization_repository=organization_repository,
        db=db,
    )


UICommonUserService = Annotated[
    UIUserService, Depends(get_user_service, use_cache=True)
]
