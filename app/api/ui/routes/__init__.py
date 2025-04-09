from fastapi import APIRouter
from .auth_route import router as auth_router
from .agent_route import router as agent_router
from .process_route import router as process_router
from .rule_route import router as rule_router
from .user_route import router as user_router

api_router = APIRouter()

api_router.include_router(router=auth_router, prefix="/auth")
api_router.include_router(router=agent_router, prefix="/agent")
api_router.include_router(router=process_router, prefix="/process")
api_router.include_router(router=rule_router, prefix="/rule")
api_router.include_router(router=user_router, prefix="/user")
