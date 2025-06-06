from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import Agent
from app.api.ui.repositories.agent_repository import (
    UIAgentRepository,
    CommonUIAgentRepository,
)
from app.api.ui.repositories.process_repository import (
    CommonProcessRepository,
    UIProcessRepository,
)


class UIAgentService:
    _agent_repository: UIAgentRepository
    _process_repository: UIProcessRepository

    def __init__(
        self,
        agent_repository: UIAgentRepository,
        process_repository: UIProcessRepository,
    ):
        self._process_repository = process_repository
        self._agent_repository = agent_repository

    async def create(self, agent: Agent):
        return await self._agent_repository.create(agent)

    async def find_all(
        self, organization_id: PydanticObjectId, embed_processes: bool = False
    ):
        if embed_processes:
            agents = await self._agent_repository.get_all_with_processes(
                organization_id=organization_id
            )
            return agents

        agents = await self._agent_repository.get_all(organization_id=organization_id)
        return agents

    async def find_by_id(
        self, agent_id: PydanticObjectId, embed_processes: bool = False
    ):
        if embed_processes:
            agent = await self._agent_repository.get_by_id_with_processes(agent_id)
            return agent

        agent = await self._agent_repository.get_by_id(agent_id)
        return agent

    async def update(self, agent: Agent):
        return await self._agent_repository.update(agent)


def get_agent_service(
    agent_repository: CommonUIAgentRepository,
    process_repository: CommonProcessRepository,
):
    return UIAgentService(
        agent_repository=agent_repository, process_repository=process_repository
    )


CommonUIAgentService = Annotated[
    UIAgentService, Depends(get_agent_service, use_cache=True)
]
