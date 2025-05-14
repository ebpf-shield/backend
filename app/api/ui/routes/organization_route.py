from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.models.organization_model import Organization
from app.api.ui.services.organization_service import CommonUIOrganizationService


router = APIRouter(tags=["organization"])


@router.post(
    "",
    description="Create a new organization",
)
async def create(
    organization: Annotated[Organization, Body()],
    organization_service: CommonUIOrganizationService,
):
    return await organization_service.create(organization)


@router.get(
    "/{organization_id}",
    description="Get organization by id",
)
async def find_by_id(
    organization_id: Annotated[PydanticObjectId, Path(description="Process id")],
    organization_service: CommonUIOrganizationService,
):
    return await organization_service.find_by_id(organization_id)
