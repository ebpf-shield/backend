from fastapi import APIRouter, Depends

from app.api.ui.services.dashboard_service import CommonDashboardService
from app.core.auth import JWTBearer

from fastapi import APIRouter, HTTPException

from app.api.models.agent_model import AgentDocument

# Attempt to import UserDocument; if not found, we return zero counts
try:
    from app.api.ui.models.user_model import UserDocument
    _HAS_USER_DOC = True
except ImportError:
    _HAS_USER_DOC = False

from app.api.models.process_model import ProcessDocument
from app.api.models.rule_model import RuleDocument

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
        # Count all agents
        total = await AgentDocument.count()
        # Count agents whose "online" field is True
        online_count = await AgentDocument.find({"online": True}).count()
        # Offline = total minus online
        offline_count = total - online_count
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to count agents: {e}")

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
    if not _HAS_USER_DOC:
        # If no UserDocument model exists, return zeros
        return {"total": 0, "active": 0, "inactive": 0}

    try:
        total = await UserDocument.count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to count users: {e}")

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
        raise HTTPException(status_code=500, detail=f"Failed to count processes: {e}")

    return {"running": running, "stopped": stopped}


@router.get("/total-rules", summary="Get counts of firewall rules (drop vs allow)")
async def total_rules():
    """
    Returns JSON:
      {
        drop: <# of RuleDocument where action == 'DROP'>,
        allow: <# where action == 'ALLOW'>
      }
    """
    try:
        drop_count = await RuleDocument.find({"action": "DROP"}).count()
        allow_count = await RuleDocument.find({"action": "ALLOW"}).count()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to count rules: {e}")

    return {"drop": drop_count, "allow": allow_count}


# ------------------------------------------------------------
# (2) Any further existing dashboard routes follow here.
# ------------------------------------------------------------
