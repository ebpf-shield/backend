from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Depends, Path, Query

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.process_model import (
    Process,
    ProcessDocument,
    ProcessWithRules,
)
from app.api.models.query.process_embed_query_model import ProcessEmbedQuery
from app.api.ui.services.process_service import CommonUIProcessService
from app.core.auth import JWTBearer

router = APIRouter(tags=["process"], dependencies=[Depends(JWTBearer())])


@router.get(
    "/agent/{agent_id}",
    description="Get all processes by agent id",
    response_model=list[ProcessDocument],
)
async def find_all_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path()],
    process_service: CommonUIProcessService,
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
    process_service: CommonUIProcessService,
):
    process = await process_service.find_by_id(process_id, embed_query.embed_rules)
    if not process:
        raise NotFoundException(detail=f"Process with id {process_id} not found")

    return process


@router.post("", description="Create a new process")
async def create(
    process: Annotated[Process, Body()], process_service: CommonUIProcessService
):
    return await process_service.create(process)


@router.patch("", description="Update a process")
async def update(
    process: Annotated[Process, Body()], process_service: CommonUIProcessService
):
    return await process_service.update(process)
