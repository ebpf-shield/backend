from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.models.agent_model import Agent
from app.api.services.agent_service import CommonAgentService

router = APIRouter(tags=["agents"])


@router.get("", description="Get all agents")
async def get_all_agents(agent_service: CommonAgentService):
    return await agent_service.find_all_agents()


@router.post("", description="Create a new agent")
async def create_agent(
    agent: Annotated[Agent, Body()], agent_service: CommonAgentService
):
    return await agent_service.create(agent)


@router.get("/{agent_id}", description="Get agent by id")
async def get_agent_by_id(
    agent_id: Annotated[PydanticObjectId, Path()], agent_service: CommonAgentService
):
    return await agent_service.find_agent_by_id(agent_id)


@router.put("/{agent_id}/rules", description="Update agent rules")
async def update_agent_rules(
    agent_id: Annotated[PydanticObjectId, Path()],
    rules: Annotated[list[PydanticObjectId], Body()],
    agent_service: CommonAgentService,
):
    return await agent_service.update_rules(agent_id, rules)
