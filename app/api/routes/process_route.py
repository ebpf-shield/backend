from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.process_model import Process, ProcessDocument, ProcessWithoutAgentId
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
    process = await process_service.find_by_id(process_id)
    if not process:
        raise NotFoundException(detail=f"Process with id {process_id} not found")

    return process


@router.post("", description="Create a new process")
async def create(
    process: Annotated[Process, Body()], process_service: CommonProcessService
):
    return await process_service.create(process)


@router.patch("", description="Update a process")
async def update(
    process: Annotated[Process, Body()], process_service: CommonProcessService
):
    return await process_service.update(process)


@router.patch("/agent/{agent_id}", description="Update processes by agent id")
async def update_many_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    processes: Annotated[list[ProcessWithoutAgentId], Body()],
    process_service: CommonProcessService,
    agent_service: CommonProcessService,
):
    agent = await agent_service.find_by_id(agent_id)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    processes_with_agent_id = [
        Process(**process.model_dump(by_alias=True), agent_id=agent_id)
        for process in processes
    ]
    res = await process_service.update_many_by_agent_id(
        agent_id, processes_with_agent_id
    )

    return {
        "deleted_count": res[0].deleted_count,
        "inserted_count": len(res[1].inserted_ids),
    }


@router.get(
    "/agent/{agent_id}/command/rules",
    description="Get all processes by agent id with rules grouped by command",
)
async def find_by_agent_with_rules_grouped_by_command(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    process_service: CommonProcessService,
):
    return await process_service.find_by_agent_with_rules_grouped_by_command(agent_id)
