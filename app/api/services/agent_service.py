from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import Agent
from app.api.repositories.agent_repository import AgentRepository, CommonAgentRepository


class AgentService:
    _agent_repository: AgentRepository

    def __init__(self, agent_repository: AgentRepository):
        self._agent_repository = agent_repository

    async def create(self, agent: Agent):
        return await self._agent_repository.create(agent)

    async def find_all_agents(self):
        return await self._agent_repository.find_all_agents()

    async def find_agent_by_id(self, agent_id: PydanticObjectId):
        return await self._agent_repository.find_agent_by_id(agent_id)


def get_agent_service(agent_repository: CommonAgentRepository):
    return AgentService(agent_repository=agent_repository)


CommonAgentService = Annotated[AgentService, Depends(get_agent_service, use_cache=True)]
