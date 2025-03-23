import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Agent(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    name: str
    created_at: datetime.datetime = Field(alias="createdAt")
    updated_at: datetime.datetime = Field(
        alias="updatedAt", default_factory=datetime.datetime.now
    )
    rules: Optional[list[PydanticObjectId]] = None
    processes: Optional[list[PydanticObjectId]] = None


class AgentDocument(Document, Agent):
    pass

    class Settings:
        name = "agents"
