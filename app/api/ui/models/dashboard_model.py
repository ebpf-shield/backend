from pydantic import BaseModel, Field

from app.api.models.process_model import ProcessStatus


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


class ProcessesStatusCount(BaseModel):
    count: int
    status: ProcessStatus


class AgentsByIsOnlineAggregation(BaseModel):
    count: int
    id: str = Field(alias="_id")
