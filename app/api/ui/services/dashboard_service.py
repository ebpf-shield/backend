from typing import Annotated

from fastapi import Depends

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


def get_dashboard_service(dashboard_repository: CommonDashboardRepository):
    return DashboardService(dashboard_repository=dashboard_repository)


CommonDashboardService = Annotated[
    DashboardService, Depends(get_dashboard_service, use_cache=True)
]
