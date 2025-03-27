from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Path

from app.api.models.process_model import Process, ProcessDocument
from app.api.services.process_service import CommonProcessService


router = APIRouter(tags=["processes"])


@router.get(
    "/agent/{agent_id}",
    description="Get all processes by agent id",
    response_model=list[ProcessDocument],
)
async def find_all_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path()], process_service: CommonProcessService
):
    return await process_service.find_all_processes_by_agent_id(agent_id)


@router.get(
    "/{process_id}",
    description="Get process by process id",
    response_model=Process,
)
async def find_by_id(
    process_id: Annotated[PydanticObjectId, Path()],
    process_service: CommonProcessService,
):
    return await process_service.find_by_id(process_id)


@router.post("", description="Create a new process")
async def create(process: ProcessDocument, process_service: CommonProcessService):
    return await process_service.create(process)


@router.patch("", description="Update a process")
async def update(process: ProcessDocument, process_service: CommonProcessService):
    return await process_service.update(process)
