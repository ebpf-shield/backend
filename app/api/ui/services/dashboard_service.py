from typing import Annotated

from fastapi import Depends

from app.api.models.process_model import ProcessStatus
from app.api.ui.repositories.dashboard_repository import (
    CommonDashboardRepository,
    DashboardRepository,
)


class DashboardService:
    _dashboard_repository: DashboardRepository

    def __init__(self, dashboard_repository: DashboardRepository):
        self._dashboard_repository = dashboard_repository

    async def common_processes(self):
        return await self._dashboard_repository.common_processes()

    async def processes_with_most_rules(self):
        return await self._dashboard_repository.processes_with_most_rules()

    async def rules_by_chain(self):
        return await self._dashboard_repository.rules_by_chain()

    async def agent_locations(self):
        return await self._dashboard_repository.agent_locations()

    async def processes_by_status(self):
        process_statuses = await self._dashboard_repository.processes_by_status()

        status_count: dict[ProcessStatus, int] = {}

        for status_entry in process_statuses:
            status_count[status_entry.status.lower()] = status_entry.count

        return status_count

    async def agents_by_is_online(self):
        agent_statuses = await self._dashboard_repository.agents_by_is_online()

        status_count: dict[str, int] = {}

        for status_entry in agent_statuses:
            status_count[status_entry.id] = status_entry.count

        status_count["total"] = sum(status_count.values())

        return status_count

    async def users_by_is_active(self):
        return await self._dashboard_repository.users_by_is_active()


def get_dashboard_service(dashboard_repository: CommonDashboardRepository):
    return DashboardService(dashboard_repository=dashboard_repository)


CommonDashboardService = Annotated[
    DashboardService, Depends(get_dashboard_service, use_cache=True)
]
