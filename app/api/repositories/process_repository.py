from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.process_model import Process, ProcessDocument


class ProcessRepository:
    def __init__(self):
        pass

    async def get_all_agent_id(self, agent_id: PydanticObjectId):
        return await ProcessDocument.find(
            {ProcessDocument.agent_id: agent_id}
        ).to_list()

    async def get_by_id(self, process_id: PydanticObjectId):
        return await ProcessDocument.get(process_id)

    async def create(self, process: Process):
        process_to_insert = ProcessDocument(**process.model_dump(by_alias=True))
        return await process_to_insert.insert()

    async def update(self, process: Process):
        process_to_update = ProcessDocument(**process.model_dump(by_alias=True))
        return await process_to_update.update()


def get_process_repository():
    return ProcessRepository()


CommonProcessRepository = Annotated[
    ProcessRepository, Depends(get_process_repository, use_cache=True)
]
