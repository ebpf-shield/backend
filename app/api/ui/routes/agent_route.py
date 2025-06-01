from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, Path, Query

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.agent_model import Agent, AgentWithProcesses
from app.api.ui.services.agent_service import CommonUIAgentService
from app.api.models.query.agent_embed_query_model import AgentEmbedQuery
from app.core.auth import (
    CommonRequestStateAuth,
    CommonRequestStateAuthWithOrg,
    JWTBearer,
)

router = APIRouter(tags=["agent"], dependencies=[Depends(JWTBearer())])


@router.get("", description="Get all agents")
async def find_all(
    agent_service: CommonUIAgentService,
    embed_query: Annotated[AgentEmbedQuery, Query()],
    auth: CommonRequestStateAuthWithOrg,
):
    return await agent_service.find_all(
        organization_id=auth.payload.organization_id,
        embed_processes=embed_query.embed_processes,
    )


@router.get(
    "/{agent_id}",
    description="Get agent by id",
    response_model=Agent | AgentWithProcesses,
)
async def find_by_id(
    agent_id: Annotated[PydanticObjectId, Path()],
    embed_query: Annotated[AgentEmbedQuery, Query()],
    agent_service: CommonUIAgentService,
    auth: CommonRequestStateAuth,
):
    agent = await agent_service.find_by_id(agent_id, embed_query.embed_processes)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    return agent
