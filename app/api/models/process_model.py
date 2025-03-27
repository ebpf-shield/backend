from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Process(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    command: str = Field(max_length=255)
    pid: int = Field(ge=0)
    agent_id: PydanticObjectId = Field(alias="agentId")


class ProcessDocument(Document, Process):
    pass

    class Settings:
        name = "processes"
