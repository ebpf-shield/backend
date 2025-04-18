from fastapi import APIRouter
from .process_route import router as process_router
from .agent_route import router as agent_router

api_router = APIRouter(prefix="/host", tags=["host"])

api_router.include_router(process_router, prefix="/process", tags=["process"])
api_router.include_router(agent_router, prefix="/agent")
