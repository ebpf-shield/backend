from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from app.api.models.rule_model import PartialRule, Rule
from app.api.ui.repositories.rule_repository import (
    CommonUIRuleRepository,
    UIRuleRepository,
)


class RuleService:
    _rule_repository: UIRuleRepository

    def __init__(self, rule_repository: UIRuleRepository):
        self._rule_repository = rule_repository

    async def find_all_by_process_id(self, process_id: PydanticObjectId):
        return await self._rule_repository.get_all_by_process_id(process_id)

    async def find_by_id(self, rule_id: PydanticObjectId):
        return await self._rule_repository.get_by_id(rule_id)

    async def create(self, rule: Rule):
        return await self._rule_repository.create(rule)

    async def update(self, rule_id: PydanticObjectId, rule: PartialRule):
        return await self._rule_repository.update(rule_id, rule)

    async def delete(self, rule_id: PydanticObjectId):
        return await self._rule_repository.delete(rule_id)


def get_rule_service(rule_repository: CommonUIRuleRepository):
    return RuleService(rule_repository=rule_repository)


CommonRuleService = Annotated[RuleService, Depends(get_rule_service, use_cache=True)]
