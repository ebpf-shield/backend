from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends
from app.api.repositories.rule_repository import CommonRuleRepository, RuleRepository


class RuleService:
    _rule_repository: RuleRepository

    def __init__(self, rule_repository: RuleRepository):
        self._rule_repository = rule_repository

    async def get_rules_by_process_id(self, process_id: PydanticObjectId):
        return await self._rule_repository.get_rules_by_process_id(process_id)

    async def get_rules_by_agent_id(self, agent_id: PydanticObjectId):
        return await self._rule_repository.get_rules_by_agent_id(agent_id)


def get_rule_service(rule_repository: CommonRuleRepository):
    return RuleService(rule_repository=rule_repository)


CommonRuleService = Annotated[RuleService, Depends(get_rule_service, use_cache=True)]
