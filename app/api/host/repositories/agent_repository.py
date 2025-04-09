from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import AgentDocument


class HostAgentRepository:
    def __init__(self):
        pass

    async def get_by_id(self, agent_id: PydanticObjectId):
        return await AgentDocument.get(agent_id)


def get_agent_repository():
    return HostAgentRepository()


CommonHostAgentRepository = Annotated[
    HostAgentRepository, Depends(get_agent_repository, use_cache=True)
]
