from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Body, Path

from app.api.errors.not_found_exception import NotFoundException
from app.api.models.rule_model import PartialRuleBody, Rule, RuleBody
from app.api.ui.services.rule_service import CommonRuleService

router = APIRouter(tags=["rule"])


@router.get("/process/{process_id}", description="Get rule by process id")
async def find_all_by_process_id(
    process_id: Annotated[PydanticObjectId, Path(description="Process id")],
    rule_service: CommonRuleService,
):
    return await rule_service.find_all_by_process_id(process_id)


@router.post("", description="Create a new rule")
async def create(rule: Annotated[RuleBody, Body()], rule_service: CommonRuleService):
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
    rule = await rule_service.find_by_id(rule_id)
    if not rule:
        raise NotFoundException(detail=f"Rule with id {rule_id} not found")

    return rule


@router.patch(
    "/{rule_id}",
    description="Update rule by id",
)
async def update(
    rule_id: Annotated[PydanticObjectId, Path(description="Rule id")],
    rule: Annotated[PartialRuleBody, Body()],
    rule_service: CommonRuleService,
):
    update_res = await rule_service.update(rule_id, rule)
    return {
        "acknowledged": update_res.acknowledged,
        "modified_count": update_res.modified_count,
    }


@router.delete("/{rule_id}", description="Delete rule by id")
async def delete(
    rule_id: Annotated[PydanticObjectId, Path(description="Rule id")],
    rule_service: CommonRuleService,
):
    res = await rule_service.delete(rule_id)
    if not res:
        raise NotFoundException(detail=f"Rule with id {rule_id} not found")

    if res.deleted_count == 0:
        raise NotFoundException(detail=f"Rule with id {rule_id} not found")

    return {
        "acknowledged": res.acknowledged,
        "deleted_count": res.deleted_count,
    }
