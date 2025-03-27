import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Agent(BaseModel):
    id: Optional[int] = Field(alias="_id", default=None)
    name: str
    created_at: datetime.datetime = Field(
        alias="createdAt", default_factory=datetime.datetime.now
    )
    updated_at: datetime.datetime = Field(
        alias="updatedAt", default_factory=datetime.datetime.now
    )
    rules: list[int] = Field(default=[])
    processes: list[int] = Field(default=[])
