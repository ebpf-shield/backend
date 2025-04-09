from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path
from fastapi.responses import JSONResponse

from app.api.errors.not_found_exception import NotFoundException
from app.api.host.services.process_service import CommonHostProcessService
from app.api.models.process_model import Process, ProcessWithoutAgentId
from app.api.ui.services.agent_service import CommonUIAgentService


router = APIRouter(tags=["process"])


@router.patch("/agent/{agent_id}", description="Update processes by agent id")
async def update_many_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    processes: Annotated[list[ProcessWithoutAgentId], Body()],
    process_service: CommonHostProcessService,
    agent_service: CommonUIAgentService,
):
    agent = await agent_service.find_by_id(agent_id)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    # Did not find a better way.
    processes_with_agent_id = []
    for process in processes:
        new_process = Process(**process.model_dump(by_alias=True))
        new_process.agent_id = agent_id
        processes_with_agent_id.append(new_process)

    res = await process_service.update_many_by_agent_id(
        agent_id, processes_with_agent_id
    )

    if len(res) == 2:
        return {
            "modified_count": res[0].modified_count,
            "inserted_count": 0,
        }

    if len(res) == 3:
        return {
            "modified_count": res[1].modified_count,
            "inserted_count": len(res[0].inserted_ids),
        }

    return JSONResponse(
        status_code=500,
        content={"detail": "An error occurred while updating processes."},
    )


@router.get(
    "/agent/{agent_id}/command/rules",
    description="Get all processes by agent id with rules grouped by command",
)
async def find_by_agent_with_rules_grouped_by_command(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    process_service: CommonHostProcessService,
):
    return await process_service.find_by_agent_with_rules_grouped_by_command(agent_id)
