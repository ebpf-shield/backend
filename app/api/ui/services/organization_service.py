from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.organization_model import Organization
from app.api.ui.repositories.organization_repository import (
    CommonUIOrganizationRepository,
    UIOrganizationRepository,
)
from app.api.ui.repositories.user_repository import (
    UICommonUserRepository,
    UIUserRepository,
)


class UIOrganizationService:
    _organization_repository: UIOrganizationRepository
    _user_repository: UIUserRepository

    def __init__(
        self,
        organization_repository: UIOrganizationRepository,
        user_repository: UIUserRepository,
    ):
        self._organization_repository = organization_repository
        self._user_repository = user_repository

    async def create(self, organization: Organization):
        return await self._organization_repository.create(organization)

    async def find_by_id(self, organization_id: PydanticObjectId):
        return await self._organization_repository.get_by_id(organization_id)

    # We for sure can make it better
    async def create_invitation(self, organization_id: PydanticObjectId, email: str):
        user = await self._user_repository.get_by_email(email)
        return await self._user_repository.update_organization_by_user_id(
            organization_id, user.id
        )


def get_organization_service(
    organization_repository: CommonUIOrganizationRepository,
    user_repository: UICommonUserRepository,
):
    return UIOrganizationService(
        organization_repository=organization_repository, user_repository=user_repository
    )


CommonUIOrganizationService = Annotated[
    UIOrganizationService, Depends(get_organization_service, use_cache=True)
]
