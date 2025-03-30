from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from app.api.models.process_model import Process
from app.api.repositories.process_repository import (
    CommonProcessRepository,
    ProcessRepository,
)


class ProcessService:
    _process_repository: ProcessRepository

    def __init__(self, process_repository: ProcessRepository):
        self._process_repository = process_repository

    async def find_all_processes_by_agent_id(self, agent_id: PydanticObjectId):
        return await self._process_repository.get_all_agent_id(agent_id)

    async def find_by_id(self, process_id: PydanticObjectId):
        return await self._process_repository.get_by_id(process_id)

    async def create(self, process: Process):
        return await self._process_repository.create(process)

    async def update(self, process: Process):
        return await self._process_repository.update(process)

    async def find_by_agent_with_rules_grouped_by_command(
        self, agent_id: PydanticObjectId
    ):
        return (
            await self._process_repository.get_by_agent_with_rules_grouped_by_command(
                agent_id
            )
        )

    async def update_many_by_agent_id(
        self, agent_id: PydanticObjectId, processes: list[Process]
    ):
        return await self._process_repository.update_many_by_agent_id(
            agent_id, processes
        )


def get_process_service(process_repository: CommonProcessRepository):
    return ProcessService(process_repository=process_repository)


CommonProcessService = Annotated[
    ProcessService, Depends(get_process_service, use_cache=True)
]
