from typing import Annotated

from fastapi import Depends


class RuleRepository:
    def __init__(self):
        pass


def get_rule_repository():
    return RuleRepository()


CommonRuleRepository = Annotated[
    RuleRepository, Depends(get_rule_repository, use_cache=True)
]
