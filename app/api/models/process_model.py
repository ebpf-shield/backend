import datetime
from enum import Enum
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field

from app.api.models.rule_model import RuleDocument


class ProcessStatus(str, Enum):
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"
    ERROR = "ERROR"


class Process(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
    )

    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    command: str = Field(max_length=255)
    count: int = Field(ge=0, le=1_000_000)
    agent_id: PydanticObjectId = Field(alias="agentId")
    created_at: datetime.datetime = Field(
        alias="createdAt", default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = Field(
        alias="updatedAt", default_factory=datetime.datetime.now
    )
    status: Optional[ProcessStatus] = Field(default=ProcessStatus.RUNNING)


class ProcessDocument(Document, Process):
    pass

    class Settings:
        name = "processes"
        keep_nulls = False


class ProcessWithRules(Process):
    rules: list[RuleDocument] = Field(alias="rules", default=[])


class ProcessByNameWithRules(BaseModel):
    command: str = Field(max_length=255)
    rules: list[RuleDocument] = Field(alias="rules", default=[])


class ProcessWithoutAgentId(Process):
    agent_id: Optional[PydanticObjectId] = Field(alias="agentId", default=None)
