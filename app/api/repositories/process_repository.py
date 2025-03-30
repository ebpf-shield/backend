import asyncio
from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import NotIn
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

from app.api.models.process_model import (
    Process,
    ProcessByNameWithRules,
    ProcessDocument,
)
from app.core.db import CommonMongoClient


class ProcessRepository:
    _client: AsyncIOMotorClient

    def __init__(self, client: CommonMongoClient):
        self._client = client

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

    async def update_many_by_agent_id(
        self, agent_id: PydanticObjectId, processes: list[Process]
    ):
        async with await self._client.start_session() as session:
            async with session.start_transaction():
                delele_by_agent_id_task = ProcessDocument.find(
                    ProcessDocument.agent_id == agent_id,
                    NotIn(
                        ProcessDocument.command,
                        [process.command for process in processes],
                    ),
                )

                insert_many_task = ProcessDocument.insert_many(
                    [ProcessDocument(**process.model_dump()) for process in processes],
                    session=session,
                )

                return await asyncio.gather(delele_by_agent_id_task, insert_many_task)

    async def get_by_agent_with_rules_grouped_by_command(
        self,
        agent_id: PydanticObjectId,
    ):
        return await ProcessDocument.aggregate(
            [
                {"$match": {"agentId": agent_id}},
                {
                    "$lookup": {
                        "from": "rules",
                        "localField": "_id",
                        "foreignField": "processId",
                        "as": "rules",
                    }
                },
                {"$unwind": {"path": "$rules"}},
                {"$group": {"_id": "$command", "rules": {"$push": "$rules"}}},
                {"$project": {"_id": 0, "command": "$_id", "rules": 1}},
            ],
            projection_model=ProcessByNameWithRules,
        ).to_list()


def get_process_repository(
    client: CommonMongoClient,
):
    return ProcessRepository(client=client)


CommonProcessRepository = Annotated[
    ProcessRepository, Depends(get_process_repository, use_cache=True)
]
