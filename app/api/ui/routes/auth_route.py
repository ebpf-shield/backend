from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import status
from app.api.errors.conflict_exception import ConflictException
from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.errors.invalid_password_exception import InvalidPasswordException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.errors.not_found_exception import NotFoundException
from app.api.ui.models.auth_model import (
    BasicTokenPayload,
    MemeberTokenPayload,
)
from app.api.ui.models.user_model import UserLogin, UserRegister
from app.api.ui.services.auth_service import (
    UICommonAuthService,
)
from app.api.ui.services.jwt_service import CommonJwtService
from app.api.ui.services.user_service import UICommonUserService
from app.core.auth import CommonRequestStateAuth, JWTBearer


router = APIRouter(tags=["auth"])


@router.post("/register", description="Register a new user")
async def register(
    user: Annotated[UserRegister, Body()],
    auth_service: UICommonAuthService,
    jwt_service: CommonJwtService,
):
    try:
        inserted_user = await auth_service.register_user(resisted_user=user)
    except EmailAlreadyExistsException as e:
        raise ConflictException(e.message)

    basic_token_payload = BasicTokenPayload(
        email=inserted_user.email,
        id=str(inserted_user.id),
        name=inserted_user.name,
    )

    token = jwt_service.generate_access_token(
        data=basic_token_payload.model_dump(by_alias=True)
    )

    return token


@router.post("/login", description="Login user")
async def login(
    user_to_login: Annotated[UserLogin, Body()],
    auth_service: UICommonAuthService,
    jwt_service: CommonJwtService,
):
    try:
        user = await auth_service.login_user(user_to_login)
    except (NoUserWithEmailException, InvalidPasswordException) as _e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid email or password"
        )

    basic_token_payload = BasicTokenPayload(
        email=user.email,
        id=str(user.id),
        name=user.name,
    )

    if user.organization_id is None:
        token_payload = basic_token_payload
    else:
        token_payload = MemeberTokenPayload(
            organization_id=str(user.organization_id),
            **basic_token_payload.model_dump(by_alias=True),
        )

    token = jwt_service.generate_access_token(
        data=token_payload.model_dump(by_alias=True)
    )

    return token


# Of course, if we have used clerk we would not need this endpoint
@router.get("/token", dependencies=[Depends(JWTBearer())])
async def token(
    auth: CommonRequestStateAuth,
    user_service: UICommonUserService,
    jwt_service: CommonJwtService,
):
    try:
        user = await user_service.get_user_by_email(auth.payload.email)

        basic_token_payload = BasicTokenPayload(
            email=user.email,
            id=str(user.id),
            name=user.name,
        )

        if user.organization_id is None:
            token_payload = basic_token_payload
        else:
            token_payload = MemeberTokenPayload(
                organization_id=str(
                    user.organization_id,
                ),
                **basic_token_payload.model_dump(by_alias=True),
            )

        token = jwt_service.generate_access_token(
            data=token_payload.model_dump(by_alias=True)
        )

        return token

    except NoUserWithEmailException as _e:
        return NotFoundException("User not found")
