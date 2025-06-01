from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.errors.conflict_exception import ConflictException
from app.api.errors.internal_server_error import IntervalServerErrorException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.errors.not_found_exception import NotFoundException
from app.api.errors.user_have_organization import UserHaveOrgException
from app.api.models.organization_model import (
    CreateOrganizationDTO,
    OrganizationInvitationDTO,
)
from app.api.ui.services.organization_service import CommonUIOrganizationService


router = APIRouter(tags=["organization"])


@router.post(
    "",
    description="Create a new organization",
)
async def create(
    organization: Annotated[CreateOrganizationDTO, Body()],
    organization_service: CommonUIOrganizationService,
):
    return await organization_service.create(organization)


@router.get(
    "/{organization_id}",
    description="Get organization by id",
)
async def find_by_id(
    organization_id: Annotated[PydanticObjectId, Path(description="Organization id")],
    organization_service: CommonUIOrganizationService,
):
    return await organization_service.find_by_id(organization_id)


@router.post("/{organization_id}/invitation")
async def create_invitation(
    organization_id: Annotated[PydanticObjectId, Path(description="Organization id")],
    body: Annotated[OrganizationInvitationDTO, Body()],
    organization_service: CommonUIOrganizationService,
):
    try:
        return await organization_service.create_invitation(organization_id, body.email)
    except NoUserWithEmailException as e:
        raise NotFoundException("User with this email does not exist") from e
    except UserHaveOrgException as e:
        raise ConflictException("User already have organization") from e
    except Exception as _e:
        raise IntervalServerErrorException
