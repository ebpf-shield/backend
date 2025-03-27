from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Path

from app.api.services.rule_service import CommonRuleService


router = APIRouter(tags=["rules"])


@router.get("/{process_id}", description="Get rule by process id")
async def find_all_by_process_id(
    process_id: Annotated[PydanticObjectId, Path(description="Process id")],
    rule_service: CommonRuleService,
):
    return await rule_service.find_all_by_process_id(process_id)
