import asyncio
from typing import Annotated
from beanie import PydanticObjectId
from fastapi import Depends
from app.api.models.process_model import Process
from app.api.repositories.process_repository import (
    CommonProcessRepository,
    ProcessRepository,
)

from pymongo.results import UpdateResult, InsertManyResult


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
    ) -> (
        tuple[UpdateResult, UpdateResult]
        | tuple[InsertManyResult, UpdateResult, UpdateResult]
    ):
        async with await self._process_repository._client.start_session() as session:
            async with session.start_transaction():
                new_processes_commands = [process.command for process in processes]
                exsiting_processes_by_commands = await self._process_repository.get_existing_by_agent_id_and_commands(
                    agent_id, new_processes_commands, session=session
                )

                existing_processes_commands = [
                    process.command for process in exsiting_processes_by_commands
                ]

                non_exsisting_processes = [
                    process
                    for process in processes
                    if process.command not in existing_processes_commands
                ]

                update_stop_task = (
                    self._process_repository.update_status_to_stopped_by_agent_id(
                        agent_id, existing_processes_commands, session=session
                    )
                )

                update_running_task = (
                    self._process_repository.update_status_to_running_for_agent_id(
                        agent_id, existing_processes_commands, session=session
                    )
                )

                if not non_exsisting_processes:
                    return await asyncio.gather(update_stop_task, update_running_task)

                insert_many_task = self._process_repository.create_many(
                    non_exsisting_processes, session=session
                )

                return await asyncio.gather(
                    insert_many_task, update_stop_task, update_running_task
                )


def get_process_service(process_repository: CommonProcessRepository):
    return ProcessService(process_repository=process_repository)


CommonProcessService = Annotated[
    ProcessService, Depends(get_process_service, use_cache=True)
]
