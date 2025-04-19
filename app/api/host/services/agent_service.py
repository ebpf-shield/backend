from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.host.repositories.agent_repository import (
    CommonHostAgentRepository,
    HostAgentRepository,
)
from app.api.models.agent_model import Agent


class HostAgentService:
    _agent_repository: HostAgentRepository

    def __init__(self, agent_repository: HostAgentRepository):
        self._agent_repository = agent_repository

    async def find_by_id(self, agent_id: PydanticObjectId):
        return await self._agent_repository.get_by_id(agent_id)

    async def create(self, agent: Agent):
        return await self._agent_repository.create(agent)


def get_agent_service(agent_repository: CommonHostAgentRepository):
    return HostAgentService(agent_repository=agent_repository)


CommonHostAgentService = Annotated[
    HostAgentService, Depends(get_agent_service, use_cache=True)
]
