from fastapi import APIRouter, Depends

from app.api.ui.services.user_service import CommonUserService
from app.core.auth import CommonRequestStateAuth, JWTBearer

router = APIRouter(tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("", description="Get all users")
async def get_all_users():
    return []


@router.post("/login", description="Login user")
async def login_user():
    return {"message": "User logged in"}


@router.get("/me", description="Get current user")
async def read_users_me(
    auth: CommonRequestStateAuth,
    user_service: CommonUserService,
):
    print(auth)
    return await user_service.get_user_by_email(auth.payload.email)
