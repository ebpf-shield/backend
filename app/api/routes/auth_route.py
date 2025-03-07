from typing import Annotated
from fastapi import APIRouter, Body
from app.api.errors.conflict_exception import ConflictException
from app.api.errors.email_already_exists_exception import EmailAlreadyExistsException
from app.api.errors.invalid_password_exception import InvalidPasswordException
from app.api.errors.no_user_with_email_exception import NoUserWithEmailException
from app.api.errors.not_found_exception import NotFoundException
from app.api.models.user_model import UserLogin, UserRegister
from app.api.services.auth_service import (
    CommonAuthService,
)
from app.api.services.jwt_service import CommonJwtService

router = APIRouter(tags=["auth"])


@router.post("/register", description="Register a new user")
async def register(
    user: Annotated[UserRegister, Body()],
    auth_service: CommonAuthService,
    jwt_service: CommonJwtService,
):
    try:
        inserted_user = await auth_service.register_user(resisted_user=user)
    except EmailAlreadyExistsException as e:
        raise ConflictException(e.message)

    token = await jwt_service.generate_token(
        data={"email": inserted_user.email, "id": str(inserted_user.id)}
    )
    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", description="Login user")
async def login(
    user_to_login: Annotated[UserLogin, Body()],
    auth_service: CommonAuthService,
    jwt_service: CommonJwtService,
):
    try:
        user = await auth_service.login_user(user_to_login)
    except (NoUserWithEmailException, InvalidPasswordException) as _e:
        raise NotFoundException("Invalid email or password")

    token = await jwt_service.generate_token({"email": user.email, "id": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/token", description="Get token")
def token():
    return {"access_token": "fake_token", "token_type": "bearer"}
