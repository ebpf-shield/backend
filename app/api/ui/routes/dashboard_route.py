from fastapi import APIRouter, Depends

from app.api.errors.internal_server_error import InternalServerErrorException
from app.api.ui.models.user_model import UserDocument
from app.api.ui.services.dashboard_service import CommonDashboardService
from app.core.auth import JWTBearer


from app.api.models.agent_model import AgentDocument


from app.api.models.process_model import ProcessDocument

# Create an APIRouter under the same prefix "/dashboard"
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
async def total_agents():
    """
    Returns JSON:
      {
        total: <# of AgentDocument in DB>,
        online: <# of AgentDocument where online == True>,
        offline: <# of AgentDocument where online == False or missing>
      }
    """
    try:
        total = await AgentDocument.count()

        online_count = await AgentDocument.find({"online": True}).count()

        offline_count = total - online_count
    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count agents: {e}")

    return {
        "total": total,
        "online": online_count,
        "offline": offline_count,
    }


@router.get("/total-users", summary="Get total/active/inactive User counts")
async def total_users():
    """
    Returns JSON:
      {
        total: <# of UserDocument> or 0 if model missing,
        active: <# active — placeholder = total>,
        inactive: <# inactive = 0>
      }
    """

    try:
        total = await UserDocument.count()
    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count users: {e}")

    # Placeholder behavior: treat all users as active
    return {"total": total, "active": total, "inactive": 0}


@router.get("/total-processes", summary="Get counts of processes by status")
async def total_processes():
    """
    Returns JSON:
      {
        running: <# of ProcessDocument where status == 'RUNNING'>,
        stopped: <# where status == 'STOPPED'>
      }
    """
    try:
        running = await ProcessDocument.find({"status": "RUNNING"}).count()
        stopped = await ProcessDocument.find({"status": "STOPPED"}).count()
    except Exception as e:
        raise InternalServerErrorException(detail=f"Failed to count processes: {e}")

    return {"running": running, "stopped": stopped}


@router.get("/agent-ips", summary="Get list of all agent external IPs")
async def agent_ips():
    """
    Returns JSON:
      [
        "203.0.113.10",
        "198.51.100.45",
        ...
      ]
    (Every AgentDocument.external_ip in the database)
    """
    try:
        # Project only the "external_ip" field from every agent
        # If AgentDocument has .external_ip as field name:
        # TODO: Please use a mongo aggregation pipeline to optimize this
        docs = await AgentDocument.find_all().to_list()
        ip_list = [a.external_ip for a in docs if getattr(a, "external_ip", None)]
        print("OK")
    except Exception as e:
        raise InternalServerErrorException(
            detail=f"Failed to fetch agent external_ips: {e}"
        )

    return ip_list
