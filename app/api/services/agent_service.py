from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import Agent, AgentWithProcesses
from app.api.repositories.agent_repository import AgentRepository, CommonAgentRepository
from app.api.repositories.process_repository import (
    CommonProcessRepository,
    ProcessRepository,
)


class AgentService:
    _agent_repository: AgentRepository
    _process_repository: ProcessRepository

    def __init__(
        self, agent_repository: AgentRepository, process_repository: ProcessRepository
    ):
        self._process_repository = process_repository
        self._agent_repository = agent_repository

    async def create(self, agent: Agent):
        return await self._agent_repository.create(agent)

    async def find_all_agents(self):
        return await self._agent_repository.get_all()

    async def find_by_id(
        self, agent_id: PydanticObjectId, embed_processes: bool = False
    ):
        agent = await self._agent_repository.get_by_id(agent_id)
        if embed_processes and agent:
            processes = await self._process_repository.get_all_agent_id(agent_id)

            agent_with_processes = AgentWithProcesses(
                **agent.model_dump(by_alias=True), processes=processes
            )

            return agent_with_processes

        return agent

    async def update(self, agent: Agent):
        return await self._agent_repository.update(agent)


def get_agent_service(
    agent_repository: CommonAgentRepository, process_repository: CommonProcessRepository
):
    return AgentService(
        agent_repository=agent_repository, process_repository=process_repository
    )


CommonAgentService = Annotated[AgentService, Depends(get_agent_service, use_cache=True)]
