from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path, Query

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.agent_model import Agent, AgentWithProcesses
from app.api.ui.services.agent_service import CommonUIAgentService
from app.api.models.query.agent_embed_query_model import AgentEmbedQuery

router = APIRouter(tags=["agent"])


@router.get("", description="Get all agents")
async def find_all(
    agent_service: CommonUIAgentService,
    embed_query: Annotated[AgentEmbedQuery, Query()],
):
    return await agent_service.find_all(embed_query.embed_processes)


@router.post("", description="Create a new agent")
async def create(
    agent: Annotated[Agent, Body()],
    agent_service: CommonUIAgentService,
):
    return await agent_service.create(agent)


@router.get(
    "/{agent_id}",
    description="Get agent by id",
    response_model=Agent | AgentWithProcesses,
)
async def find_by_id(
    agent_id: Annotated[PydanticObjectId, Path()],
    embed_query: Annotated[AgentEmbedQuery, Query()],
    agent_service: CommonUIAgentService,
):
    agent = await agent_service.find_by_id(agent_id, embed_query.embed_processes)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    return agent


@router.patch("/{agent_id}", description="Update agent by id")
async def update(
    agent_id: Annotated[PydanticObjectId, Path()],
    agent: Annotated[Agent, Body()],
    agent_service: CommonUIAgentService,
):
    agent.id = agent_id
    return await agent_service.update(agent)
