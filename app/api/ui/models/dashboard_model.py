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


class AgentLocationProjection(BaseModel):
    latitude: float
    longitude: float
    ip: str

    class Settings:
        projection = {
            "latitude": "$geolocationProperties.latitude",
            "longitude": "$geolocationProperties.longitude",
            "ip": "$geolocationProperties.ip",
        }
