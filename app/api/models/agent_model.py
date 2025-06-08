import datetime as dt
from typing import Optional
from beanie import Document, PydanticObjectId
from faker import Faker
from pydantic import BaseModel, Field

from app.api.models.process_model import ProcessDocument

faker = Faker()


class Agent(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    name: Optional[str] = Field(default_factory=faker.name)
    created_at: dt.datetime = Field(alias="createdAt", default_factory=dt.datetime.now)
    updated_at: dt.datetime = Field(alias="updatedAt", default_factory=dt.datetime.now)
    online: bool = True
    processes_to_exclude: list[str] = Field(
        alias="processesToExclude", default=["kworker"]
    )
    external_ip: Optional[str] = None
    organization_id: PydanticObjectId = Field(alias="organizationId")


class AgentDocument(Document, Agent):
    pass

    class Settings:
        name = "agents"
        keep_nulls = False


class AgentWithProcesses(Agent):
    processes: list[ProcessDocument] = Field(alias="processes", default=[])
