from typing import Annotated
from fastapi import APIRouter, Body

from app.api.models.agent_model import Agent
from app.api.ui.repositories.agent_repository import CommonUIAgentRepository


router = APIRouter()


@router.post("/", description="create the agent")
async def create(
    agent: Annotated[Agent, Body()], agent_service: CommonUIAgentRepository
):
    return await agent_service.create(agent)
