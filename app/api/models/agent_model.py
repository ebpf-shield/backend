import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Agent(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    name: str
    created_at: datetime.datetime = Field(
        alias="createdAt", default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = Field(
        alias="updatedAt", default_factory=datetime.datetime.now
    )
    rules: list[PydanticObjectId] = Field(default=[])
    processes: list[PydanticObjectId] = Field(default=[])


class AgentDocument(Document, Agent):
    pass

    class Settings:
        name = "agents"
