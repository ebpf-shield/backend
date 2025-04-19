from typing import Annotated

from anyio import Path
from beanie import PydanticObjectId
from fastapi import APIRouter, Body
from pymongo.errors import DuplicateKeyError

from app.api.errors.conflict_exception import ConflictException
from app.api.host.models.agent.exsits_by_id_dto import (
    ExistsByIdResponseDto,
)
from app.api.host.repositories.agent_repository import CommonHostAgentRepository
from app.api.models.agent_model import Agent

router = APIRouter()


@router.post("/", description="create the agent")
async def create(
    agent: Annotated[Agent, Body()], agent_service: CommonHostAgentRepository
):
    try:
        return await agent_service.create(agent)
    except DuplicateKeyError as _duplicate_key_error:
        return ConflictException(
            detail="Agent with the same id already exists",
        )


@router.get(
    "/exists/{agent_id}",
    description="check if the agent with a specific id exists",
    response_model=ExistsByIdResponseDto,
)
async def exists(
    agent_id: Annotated[PydanticObjectId, Path()],
    agent_service: CommonHostAgentRepository,
):
    agent = await agent_service.get_by_id(agent_id)
    return ExistsByIdResponseDto(
        exists=agent is not None,
    )
