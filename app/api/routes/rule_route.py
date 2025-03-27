from typing import Annotated
from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.models.rule_model import Rule
from app.api.services.rule_service import CommonRuleService


router = APIRouter(tags=["rules"])


@router.get("/process/{process_id}", description="Get rule by process id")
async def find_all_by_process_id(
    process_id: Annotated[PydanticObjectId, Path(description="Process id")],
    rule_service: CommonRuleService,
):
    return await rule_service.find_all_by_process_id(process_id)


@router.post("", description="Create a new rule")
async def create(rule: Annotated[Rule, Body()], rule_service: CommonRuleService):
    return await rule_service.create(rule)


@router.get(
    "/{rule_id}",
    description="Get rule by id",
    response_model=Rule,
)
async def find_by_id(
    rule_id: Annotated[PydanticObjectId, Path(description="Rule id")],
    rule_service: CommonRuleService,
):
    return await rule_service.find_by_id(rule_id)


@router.patch(
    "/{rule_id}",
    description="Update rule by id",
    response_model=Rule,
)
async def update(
    rule_id: Annotated[PydanticObjectId, Path(description="Rule id")],
    rule: Annotated[Rule, Body()],
    rule_service: CommonRuleService,
):
    return await rule_service.update(rule_id, rule)
