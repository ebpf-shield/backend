import datetime as dt
from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Organization(BaseModel):
    id: PydanticObjectId = Field(alias="_id", default_factory=PydanticObjectId)
    name: str = Field(min_length=4, max_length=50)
    description: Optional[str] = Field(min_length=4, max_length=50, default=None)
    created_at: dt.datetime = Field(alias="createdAt", default_factory=dt.datetime.now)
    updated_at: dt.datetime = Field(alias="updatedAt", default_factory=dt.datetime.now)


class OrganizationDocument(Document, Organization):
    pass

    class Settings:
        name = "organizations"
        keep_nulls = False


class CreateOrganizationDTO(Organization):
    id: Optional[PydanticObjectId] = None
