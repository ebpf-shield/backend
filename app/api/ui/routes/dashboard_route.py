from fastapi import APIRouter

from app.api.ui.services.dashboard_service import CommonDashboardService


router = APIRouter(tags=["dashboard"])


@router.get("/common-processes", description="Most common processes by count")
async def common_processes(dashboard_service: CommonDashboardService):
    return await dashboard_service.common_processes()


@router.get(
    "/processes-with-most-rules", description="Processes with most rules by count"
)
async def processes_with_most_rules(dashboard_service: CommonDashboardService):
    return await dashboard_service.processes_with_most_rules()


@router.get("/rules-by-chain", description="Group rules by chain and count")
async def rules_by_chain(dashboard_service: CommonDashboardService):
    return await dashboard_service.rules_by_chain()
