from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import In, NotIn, Set
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorClientSession
from pymongo.results import UpdateResult

from app.api.models.process_model import (
    Process,
    ProcessByNameWithRules,
    ProcessDocument,
    ProcessStatus,
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

    async def get_existing_by_agent_id_and_commands(
        self,
        agent_id: PydanticObjectId,
        commands: list[str],
        session: AsyncIOMotorClientSession,
    ) -> list[ProcessDocument]:
        return await ProcessDocument.find_many(
            ProcessDocument.agent_id == agent_id,
            In(ProcessDocument.command, commands),
            session=session,
        ).to_list()

    async def update_status_to_stopped_by_agent_id(
        self,
        agent_id: PydanticObjectId,
        active_commands: list[str],
        session: AsyncIOMotorClientSession,
    ) -> UpdateResult:
        return await ProcessDocument.find(
            ProcessDocument.agent_id == agent_id,
            NotIn(ProcessDocument.command, active_commands),
        ).update_many(
            Set({ProcessDocument.status: ProcessStatus.STOPPED}),
            session=session,
        )

    async def create_many(
        self, processes: list[Process], session: AsyncIOMotorClientSession
    ):
        documents = [ProcessDocument(**p.model_dump()) for p in processes]
        return await ProcessDocument.insert_many(documents, session=session)

    async def update_status_to_running_for_agent_id(
        self,
        agent_id: PydanticObjectId,
        active_commands: list[str],
        session: AsyncIOMotorClientSession,
    ) -> UpdateResult:
        return await ProcessDocument.find(
            ProcessDocument.agent_id == agent_id,
            ProcessDocument.status != ProcessStatus.RUNNING,
            In(ProcessDocument.command, active_commands),
        ).update_many(
            Set({ProcessDocument.status: ProcessStatus.RUNNING}),
            session=session,
        )

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
