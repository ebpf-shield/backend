from beanie import PydanticObjectId
from pydantic import BaseModel, Field

from app.api.models.process_model import InnerProcess


class UpdateManyByAgentIdDTO(BaseModel):
    processes: list[InnerProcess]
    organization_id: PydanticObjectId = Field(alias="organizationId")
