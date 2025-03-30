from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path, Query
from fastapi.responses import JSONResponse

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.process_model import (
    Process,
    ProcessDocument,
    ProcessWithRules,
    ProcessWithoutAgentId,
)
from app.api.models.query.process_embed_query_model import ProcessEmbedQuery
from app.api.services.agent_service import CommonAgentService
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
    response_model=Process | ProcessWithRules,
)
async def find_by_id(
    process_id: Annotated[PydanticObjectId, Path()],
    embed_query: Annotated[ProcessEmbedQuery, Query()],
    process_service: CommonProcessService,
):
    process = await process_service.find_by_id(process_id, embed_query.embed_rules)
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
    agent_service: CommonAgentService,
):
    agent = await agent_service.find_by_id(agent_id)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    processes_with_agent_id = []
    for process in processes:
        new_process = Process(**process.model_dump(by_alias=True))
        new_process.agent_id = agent_id
        processes_with_agent_id.append(new_process)

    res = await process_service.update_many_by_agent_id(
        agent_id, processes_with_agent_id
    )

    if len(res) == 2:
        return {
            "modified_count": res[0].modified_count,
            "inserted_count": 0,
        }

    if len(res) == 3:
        return {
            "modified_count": res[1].modified_count,
            "inserted_count": len(res[0].inserted_ids),
        }

    return JSONResponse(
        status_code=500,
        content={"detail": "An error occurred while updating processes."},
    )


@router.get(
    "/agent/{agent_id}/command/rules",
    description="Get all processes by agent id with rules grouped by command",
)
async def find_by_agent_with_rules_grouped_by_command(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    process_service: CommonProcessService,
):
    return await process_service.find_by_agent_with_rules_grouped_by_command(agent_id)
