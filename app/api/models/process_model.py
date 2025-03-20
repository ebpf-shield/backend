from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Process(BaseModel):
    _id: Optional[PydanticObjectId] = Field(alias="_id")
    command: str = Field(max_length=255)
    agent_id: PydanticObjectId = Field(alias="agentId")
    pid: int = Field(ge=0)


class ProcessDocument(Document, Process):
    pass

    class Settings:
        name = "processes"
