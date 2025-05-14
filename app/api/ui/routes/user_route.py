from fastapi import APIRouter, Depends

from app.api.ui.services.user_service import CommonUserService
from app.core.auth import CommonRequestStateAuth, JWTBearer

router = APIRouter(tags=["user"], dependencies=[Depends(JWTBearer())])


@router.get("/me", description="Get current user")
async def read_users_me(
    auth: CommonRequestStateAuth,
    user_service: CommonUserService,
):
    return await user_service.get_user_by_email(auth.payload.email)
