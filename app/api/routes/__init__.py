from fastapi import APIRouter
from .auth_route import router as auth_router
from .agent_route import router as agent_router

api_router = APIRouter()

api_router.include_router(router=auth_router, prefix="/auth")
api_router.include_router(router=agent_router, prefix="/agent")
