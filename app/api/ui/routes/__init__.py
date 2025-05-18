from fastapi import APIRouter

from .auth_route import router as auth_router
from .agent_route import router as agent_router
from .process_route import router as process_router
from .rule_route import router as rule_router
from .user_route import router as user_router
from .dashboard_route import router as dashboard_router
from .organization_route import router as organization_router

api_router = APIRouter(prefix="/ui", tags=["ui"])

api_router.include_router(router=auth_router, prefix="/auth")
api_router.include_router(router=agent_router, prefix="/agent")
api_router.include_router(router=process_router, prefix="/process")
api_router.include_router(router=rule_router, prefix="/rule")
api_router.include_router(router=user_router, prefix="/user")
api_router.include_router(router=dashboard_router, prefix="/dashboard")
api_router.include_router(router=organization_router, prefix="/organization")
