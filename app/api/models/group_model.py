import datetime as dt
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Group(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    name: str = Field(min_length=4, max_length=50)
    description: str = Field(min_length=4, max_length=50)
    created_at: dt.datetime = Field(alias="createdAt", default_factory=dt.datetime.now)
    updated_at: dt.datetime = Field(alias="createdAt", default_factory=dt.datetime.now)


class GroupDocument(Document, Group):
    pass

    class Settings:
        name = "groups"
        keep_nulls = False
