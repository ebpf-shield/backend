from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.models.organization_model import Organization, OrganizationDocument


class UIOrganizationRepository:
    def __init__(self):
        pass

    async def create(
        self, organization: Organization, session: AsyncIOMotorClient = None
    ):
        organization_to_insert = OrganizationDocument(
            **organization.model_dump(by_alias=True)
        )
        return await organization_to_insert.insert(session=session)

    async def get_by_id(self, organization_id: PydanticObjectId):
        return await OrganizationDocument.get(organization_id)


def get_organization_repository() -> UIOrganizationRepository:
    return UIOrganizationRepository()


CommonUIOrganizationRepository = Annotated[
    UIOrganizationRepository, Depends(get_organization_repository, use_cache=True)
]
