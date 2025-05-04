from pydantic import BaseModel


class CommonProcessesInAgentsAggregation(BaseModel):
    name: str
    count: int


class ProcessesWithMostRulesAggregation(BaseModel):
    name: str
    rulesCount: int
