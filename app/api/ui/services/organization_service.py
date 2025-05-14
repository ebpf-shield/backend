from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from app.api.models.organization_model import Organization
from app.api.ui.repositories.organization_repository import (
    CommonUIOrganizationRepository,
    UIOrganizationRepository,
)


class UIOrganizationService:
    _organization_repository: UIOrganizationRepository

    def __init__(self, organization_repository: UIOrganizationRepository):
        self._organization_repository = organization_repository

    async def create(self, organization: Organization):
        return await self._organization_repository.create(organization)

    async def find_by_id(self, organization_id: PydanticObjectId):
        return await self._organization_repository.get_by_id(organization_id)


def get_organization_service(organization_repository: CommonUIOrganizationRepository):
    return UIOrganizationService(organization_repository=organization_repository)


CommonUIOrganizationService = Annotated[
    UIOrganizationService, Depends(get_organization_service, use_cache=True)
]
