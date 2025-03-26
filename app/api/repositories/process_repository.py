from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.process_model import Process, ProcessDocument


class ProcessRepository:
    def __init__(self):
        pass

    async def get_all_processes_by_agent_id(self, agent_id: PydanticObjectId):
        return await ProcessDocument.find(
            {ProcessDocument.agent_id: agent_id}
        ).to_list()


def get_process_repository():
    return ProcessRepository()


CommonProcessRepository = Annotated[
    ProcessRepository, Depends(get_process_repository, use_cache=True)
]
