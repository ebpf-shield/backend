from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Process(BaseModel):
    command: str = Field(max_length=255)
    agent_id: PydanticObjectId
