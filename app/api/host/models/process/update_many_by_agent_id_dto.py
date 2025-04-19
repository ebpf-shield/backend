from pydantic import BaseModel

from app.api.models.process_model import ProcessWithoutAgentId


class UpdateManyByAgentIdDTO(BaseModel):
    processes: list[ProcessWithoutAgentId]
