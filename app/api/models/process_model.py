import datetime
from enum import Enum
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.api.models.rule_model import RuleDocument


class ProcessStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class Process(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    command: str = Field(max_length=255)
    pid: int = Field(ge=0)
    agent_id: PydanticObjectId = Field(alias="agentId")
    created_at: datetime.datetime = Field(
        alias="createdAt", default_factory=datetime.datetime.now
    )
    status: Optional[ProcessStatus] = Field(default=ProcessStatus.RUNNING)


class ProcessDocument(Document, Process):
    pass

    class Settings:
        name = "processes"


class ProcessWithRules(Process):
    rules: list[RuleDocument] = Field(alias="rules", default=[])
