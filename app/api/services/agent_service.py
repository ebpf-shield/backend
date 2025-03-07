from typing import Annotated

from fastapi import Depends

from app.api.models.agent_model import Agent
from app.api.repositories.agent_repository import AgentRepository, CommonAgentRepository


class AgentService:
    _agent_repository: AgentRepository

    def __init__(self, agent_repository: AgentRepository):
        self._agent_repository = agent_repository

    async def create(self, agent: Agent):
        return await self._agent_repository.create(agent)


def get_agent_service(agent_repository: CommonAgentRepository):
    return AgentService(agent_repository=agent_repository)


CommonAgentService = Annotated[AgentService, Depends(get_agent_service, use_cache=True)]
