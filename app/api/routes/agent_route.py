from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path, Query

from app.api.models.agent_model import Agent, AgentWithProcesses
from app.api.services.agent_service import CommonAgentService
from app.api.models.query.agent_embed_query_model import AgentEmbedQuery

router = APIRouter(tags=["agents"])


@router.get("", description="Get all agents")
async def find_all(agent_service: CommonAgentService):
    return await agent_service.find_all_agents()


@router.post("", description="Create a new agent")
async def create(
    agent: Annotated[Agent, Body()],
    agent_service: CommonAgentService,
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
    agent_service: CommonAgentService,
):
    return await agent_service.find_by_id(agent_id, embed_query.embed_processes)


@router.patch("/{agent_id}", description="Update agent by id")
async def update(
    agent_id: Annotated[PydanticObjectId, Path()],
    agent: Annotated[Agent, Body()],
    agent_service: CommonAgentService,
):
    agent.id = agent_id
    return await agent_service.update(agent)
