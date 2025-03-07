from typing import Annotated

from fastapi import Depends
from app.api.repositories.rule_repository import CommonRuleRepository, RuleRepository


class RuleService:
    _rule_repository: RuleRepository

    def __init__(self, rule_repository: RuleRepository):
        self._rule_repository = rule_repository


def get_rule_service(rule_repository: CommonRuleRepository):
    return RuleService(rule_repository=rule_repository)


CommonRuleService = Annotated[RuleService, Depends(get_rule_service, use_cache=True)]
