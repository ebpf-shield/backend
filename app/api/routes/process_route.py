from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Path

from app.api.models.process_model import ProcessDocument
from app.api.services.process_service import CommonProcessService


router = APIRouter(tags=["processes"])


@router.get(
    "/{agent_id}",
    description="Get all processes by agent id",
    response_model=list[ProcessDocument],
)
async def get_all_processes_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path()], process_service: CommonProcessService
):
    return await process_service.get_all_processes_by_agent_id(agent_id)
