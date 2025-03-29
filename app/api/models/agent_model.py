import datetime
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.api.models.process_model import ProcessDocument


class Agent(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    name: str
    created_at: datetime.datetime = Field(
        alias="createdAt", default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = Field(
        alias="updatedAt", default_factory=datetime.datetime.now
    )
    online: bool = False


class AgentDocument(Document, Agent):
    pass

    class Settings:
        name = "agents"


class AgentWithProcesses(Agent):
    processes: list[ProcessDocument] = Field(alias="processes", default=[])
