from pydantic import BaseModel, Field


class CommonProcessesInAgentsAggregation(BaseModel):
    name: str
    count: int


class ProcessesWithMostRulesAggregation(BaseModel):
    name: str
    rulesCount: int


class RulesByChainAggregation(BaseModel):
    id: str = Field(alias="_id")
    count: int
