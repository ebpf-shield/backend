from fastapi import APIRouter
from .auth_route import router as auth_router

api_router = APIRouter()

api_router.include_router(router=auth_router, prefix="/auth")
