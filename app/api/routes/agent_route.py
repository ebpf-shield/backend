from typing import Annotated
from fastapi import APIRouter, Body

from app.api.models.agent_model import Agent
from app.api.services.agent_service import CommonAgentService

router = APIRouter(tags=["agents"])


@router.get("", description="Get all agents")
async def get_all_agents():
    return "a"


@router.post("", description="Create a new agent")
async def create_agent(
    agent: Annotated[Agent, Body()], agent_service: CommonAgentService
):
    return await agent_service.create(agent)
