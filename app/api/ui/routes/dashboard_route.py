from fastapi import APIRouter, Depends

from app.api.errors.internal_server_error import InternalServerErrorException
from app.api.ui.services.dashboard_service import CommonDashboardService
from app.core.auth import JWTBearer

router = APIRouter(tags=["dashboard"], dependencies=[Depends(JWTBearer())])


@router.get("/common-processes", description="Most common processes by count")
async def common_processes(dashboard_service: CommonDashboardService):
    return await dashboard_service.common_processes()


@router.get(
    "/processes-with-most-rules", description="Processes with most rules by count"
)
async def processes_with_most_rules(dashboard_service: CommonDashboardService):
    return await dashboard_service.processes_with_most_rules()


# TODO: We can add another field of total.
@router.get("/rules-by-chain", description="Group rules by chain and count")
async def rules_by_chain(dashboard_service: CommonDashboardService):
    return await dashboard_service.rules_by_chain()


@router.get("/total-agents", summary="Get total/online/offline Agent counts")
async def total_agents(
    dashboard_service: CommonDashboardService,
):
    """
    Returns JSON:
      {
        total: <# of AgentDocument in DB>,
        online: <# of AgentDocument where online == True>,
        offline: <# of AgentDocument where online == False or missing>
      }
    """
    try:
        return await dashboard_service.agents_by_is_online()

    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count agents: {e}")


@router.get("/total-users", summary="Get total/active/inactive User counts")
async def total_users(
    dashboard_service: CommonDashboardService,
):
    """
    Returns JSON:
      {
        total: <# of UserDocument> or 0 if model missing,
        active: <# active — placeholder = total>,
        inactive: <# inactive = 0>
      }
    """

    try:
        total = await dashboard_service.users_by_is_active()
    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count users: {e}")

    # Placeholder behavior: treat all users as active
    return {"total": total, "active": total, "inactive": 0}


@router.get("/processes-by-status", summary="Get counts of processes by status")
async def processes_by_status(dashboard_service: CommonDashboardService):
    """
    Returns JSON:
      {
        running: <# of ProcessDocument where status == 'RUNNING'>,
        stopped: <# where status == 'STOPPED'>
      }
    """
    try:
        statusses_count = await dashboard_service.processes_by_status()
    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count processes: {e}")

    return statusses_count


@router.get("/agent-locations", summary="Get list of all agent locations")
async def agent_ips(dashboard_service: CommonDashboardService):
    try:
        return await dashboard_service.agent_locations()
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Failed to fetch agent locations: {e}"
        )
