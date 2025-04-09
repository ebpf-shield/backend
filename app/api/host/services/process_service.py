import asyncio
from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from pymongo.results import InsertManyResult, UpdateResult

from app.api.host.repositories.process_repository import HostProcessRepository
from app.api.models.process_model import Process


class HostProcessService:
    _process_repository: HostProcessRepository

    def __init__(self, process_repository: HostProcessRepository):
        self._process_repository = process_repository

    async def update_many_by_agent_id(
        self, agent_id: PydanticObjectId, processes: list[Process]
    ) -> (
        tuple[UpdateResult, UpdateResult]
        | tuple[InsertManyResult, UpdateResult, UpdateResult]
    ):
        """
        Update process statuses and insert new processes for a specified agent automically.

        This method performs the following operations in a single transaction:
        - Updates the status of existing processes for the given agent by setting them to
            "stopped" and "running" as appropriate.
        - Inserts any processes from the provided list that do not already exist in the database.

        The use of a transaction ensures that either all operations succeed or none are applied,
        maintaining data consistency.

        Args
            agent_id (PydanticObjectId): The ID of the agent whose processes are being updated.
            processes (list[Process]): A list of Process objects to be updated or inserted.

        Returns

            tuple[UpdateResult, UpdateResult]
                If there are no new processes to insert, the method returns a tuple containing
                two UpdateResult objects corresponding to the outcomes of the "stopped" and "running"
                status updates.

            tuple[InsertManyResult, UpdateResult, UpdateResult]
                If new processes are inserted, the method returns a tuple with three objects:
                the first being an InsertManyResult representing the insertion result, followed by
                two UpdateResult objects for the "stopped" and "running" updates, respectively.
        """
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

    async def find_by_agent_with_rules_grouped_by_command(
        self, agent_id: PydanticObjectId
    ):
        return (
            await self._process_repository.get_by_agent_with_rules_grouped_by_command(
                agent_id
            )
        )


def get_process_service():
    return HostProcessService()


CommonHostProcessService = Annotated[
    HostProcessService, Depends(get_process_service, use_cache=True)
]
