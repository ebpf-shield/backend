from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession

from app.api.models.process_model import (
    Process,
    ProcessDocument,
    ProcessWithRules,
)
from app.core.db import CommonDBClientManager


class UIProcessRepository:
    _client: AsyncIOMotorClient

    def __init__(self, client: CommonDBClientManager):
        self._client = client

    async def get_all_agent_id(self, agent_id: PydanticObjectId):
        return await ProcessDocument.find(
            {ProcessDocument.agent_id: agent_id}
        ).to_list()

    async def get_by_id(self, process_id: PydanticObjectId):
        return await ProcessDocument.get(process_id)

    async def get_by_id_with_rules(self, process_id: PydanticObjectId):
        [process] = await ProcessDocument.aggregate(
            [
                {"$match": {"_id": process_id}},
                {
                    "$lookup": {
                        "from": "rules",
                        "localField": "_id",
                        "foreignField": "processId",
                        "as": "rules",
                    }
                },
            ],
            projection_model=ProcessWithRules,
        ).to_list()

        return process

    async def create(self, process: Process):
        process_to_insert = ProcessDocument(**process.model_dump(by_alias=True))
        return await process_to_insert.insert()

    async def update(self, process: Process):
        process_to_update = ProcessDocument(**process.model_dump(by_alias=True))
        return await process_to_update.update()

    async def create_many(
        self, processes: list[Process], session: AsyncIOMotorClientSession
    ):
        documents = [ProcessDocument(**p.model_dump()) for p in processes]
        return await ProcessDocument.insert_many(documents, session=session)


def get_process_repository(
    client: CommonDBClientManager,
):
    return UIProcessRepository(client=client)


CommonProcessRepository = Annotated[
    UIProcessRepository, Depends(get_process_repository, use_cache=True)
]
