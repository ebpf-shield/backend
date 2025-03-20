from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.rule_model import Rule, RuleDocument


class RuleRepository:
    def __init__(self):
        pass

    async def get_rules_by_process_id(self, process_id: PydanticObjectId):
        return await RuleDocument.find({RuleDocument.process_id: process_id}).to_list()

    async def get_rules_by_agent_id(self, agent_id: PydanticObjectId):
        return await RuleDocument.find({RuleDocument.agent_id: agent_id}).to_list()

    async def create(self, rule: Rule):
        rule_to_insert = RuleDocument(**rule.model_dump(by_alias=True))
        return await rule_to_insert.insert()

    async def update(self, rule: Rule):
        rule_to_update = RuleDocument(**rule.model_dump(by_alias=True))
        return await rule_to_update.update()


def get_rule_repository():
    return RuleRepository()


CommonRuleRepository = Annotated[
    RuleRepository, Depends(get_rule_repository, use_cache=True)
]
