from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.rule_model import (
    PartialInputRule,
    PartialOutputRule,
    PartialRule,
    Rule,
    RuleChain,
    RuleDocument,
)


class UIRuleRepository:
    def __init__(self):
        pass

    async def get_all_by_process_id(self, process_id: PydanticObjectId):
        return await RuleDocument.find({RuleDocument.process_id: process_id}).to_list()

    async def get_by_id(self, rule_id: PydanticObjectId):
        return await RuleDocument.get(rule_id)

    async def create(self, rule: Rule):
        rule_to_insert = RuleDocument(**rule.model_dump(by_alias=True))
        return await rule_to_insert.insert()

    async def update(self, rule_id: PydanticObjectId, rule: PartialRule):
        rule_to_update = rule.model_dump(by_alias=True, exclude_unset=True)
        found_rule = await RuleDocument.get(rule_id)

        try:
            if found_rule.chain == RuleChain.INPUT:
                rule_to_update = PartialInputRule(**rule_to_update).model_dump(
                    by_alias=True, exclude_unset=True, exclude_none=True
                )
            elif found_rule.chain == RuleChain.OUTPUT:
                rule_to_update = PartialOutputRule(**rule_to_update).model_dump(
                    by_alias=True, exclude_unset=True, exclude_none=True
                )
        except Exception as _e:
            pass

        return await RuleDocument.find_one({RuleDocument.id: rule_id}).update_one(
            {"$set": rule_to_update}
        )

    async def delete(self, rule_id: PydanticObjectId):
        return await RuleDocument.find_one({RuleDocument.id: rule_id}).delete_one()


def get_rule_repository():
    return UIRuleRepository()


CommonUIRuleRepository = Annotated[
    UIRuleRepository, Depends(get_rule_repository, use_cache=True)
]
