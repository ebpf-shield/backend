from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from app.api.repositories.process_repository import (
    CommonProcessRepository,
    ProcessRepository,
)


class ProcessService:
    _process_repository: ProcessRepository

    def __init__(self, process_repository: ProcessRepository):
        self._process_repository = process_repository

    async def find_all_processes_by_agent_id(self, agent_id: PydanticObjectId):
        return await self._process_repository.get_all_processes_by_agent_id(agent_id)


def get_process_service(process_repository: CommonProcessRepository):
    return ProcessService(process_repository=process_repository)


CommonProcessService = Annotated[
    ProcessService, Depends(get_process_service, use_cache=True)
]
