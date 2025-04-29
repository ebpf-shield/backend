from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path
from fastapi.responses import JSONResponse

from app.api.errors.not_found_exception import NotFoundException
from app.api.host.models.process.update_many_by_agent_id_dto import (
    UpdateManyByAgentIdDTO,
)
from app.api.host.services.agent_service import CommonHostAgentService
from app.api.host.services.process_service import CommonHostProcessService


router = APIRouter(tags=["process"])


@router.patch("/agent/{agent_id}", description="Update processes by agent id")
async def update_many_by_agent_id(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    body: Annotated[UpdateManyByAgentIdDTO, Body()],
    process_service: CommonHostProcessService,
    agent_service: CommonHostAgentService,
):
    agent = await agent_service.find_by_id(agent_id)
    if not agent:
        raise NotFoundException(detail=f"Agent with id {agent_id} not found")

    res = await process_service.update_many_by_agent_id(agent_id, body.processes)

    if len(res) == 2:
        return {
            "stopped_count": res[0].modified_count,
            "started_count": res[1].modified_count,
        }

    if len(res) == 3:
        return {
            "inserted_count": len(res[0].inserted_ids),
            "sttoped_count": res[1].modified_count,
            "started_count": res[2].modified_count,
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
