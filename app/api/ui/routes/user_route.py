from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends

from app.api.errors.conflict_exception import ConflictException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.errors.not_found_exception import NotFoundException
from app.api.errors.user_have_organization import UserHaveOrgException
from app.api.models.organization_model import CreateOrganizationDTO
from app.api.ui.services.user_service import UICommonUserService
from app.core.auth import CommonRequestStateAuth, JWTBearer

router = APIRouter(tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("/me", description="Get current user")
async def read_users_me(
    auth: CommonRequestStateAuth,
    user_service: UICommonUserService,
):
    try:
        return await user_service.get_user_by_email(auth.payload.email)
    except NoUserWithEmailException as e:
        raise NotFoundException(e.message)


@router.post("/organization", description="Create organization and assign to user")
async def create_organization(
    auth: CommonRequestStateAuth,
    user_service: UICommonUserService,
    organization: Annotated[CreateOrganizationDTO, Body()],
):
    try:
        id = PydanticObjectId(auth.payload.id)
        user = await user_service.get_user_by_id(id)

        if user.organization_id:
            raise UserHaveOrgException

        return await user_service.create_organization_by_user_id(user.id, organization)

    except NoUserWithEmailException as e:
        raise NotFoundException(e.message)

    except UserHaveOrgException as e:
        raise ConflictException("User already has an organization")
