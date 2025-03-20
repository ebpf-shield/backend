from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Path

from app.api.services.rule_service import CommonRuleService


router = APIRouter(tags=["rules"])


@router.get("/{agent_id}", description="Get all rules by agent")
async def get_all_rules_by_agent(
    agent_id: Annotated[PydanticObjectId, Path(description="Agent id")],
    rule_service: CommonRuleService,
):
    return await rule_service.get_rules_by_agent_id(agent_id)


@router.get("/{process_id}", description="Get rule by process id")
async def get_rule_by_process_id(
    process_id: Annotated[PydanticObjectId, Path(description="Process id")],
    rule_service: CommonRuleService,
):
    return await rule_service.get_rules_by_process_id(process_id)
