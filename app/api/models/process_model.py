from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field

from app.api.models.rule_model import RuleDocument


class Process(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    command: str = Field(max_length=255)
    pid: int = Field(ge=0)
    agent_id: PydanticObjectId = Field(alias="agentId")


class ProcessDocument(Document, Process):
    pass

    class Settings:
        name = "processes"


class ProcessWithRules(Process):
    rules: list[RuleDocument] = Field(alias="rules", default=[])
