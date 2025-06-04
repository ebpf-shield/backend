from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from app.api.ui.repositories.process_repository import (
    CommonProcessRepository,
    UIProcessRepository,
)


class UIProcessService:
    _process_repository: UIProcessRepository

    def __init__(self, process_repository: UIProcessRepository):
        self._process_repository = process_repository

    async def find_all_processes_by_agent_id(self, agent_id: PydanticObjectId):
        return await self._process_repository.get_all_agent_id(agent_id)

    async def find_by_id(self, process_id: PydanticObjectId, embed_rules: bool = False):
        if embed_rules:
            return await self._process_repository.get_by_id_with_rules(process_id)

        return await self._process_repository.get_by_id(process_id)


def get_process_service(process_repository: CommonProcessRepository):
    return UIProcessService(process_repository=process_repository)


CommonUIProcessService = Annotated[
    UIProcessService, Depends(get_process_service, use_cache=True)
]
