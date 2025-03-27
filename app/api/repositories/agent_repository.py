from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import Agent, AgentDocument


class AgentRepository:
    def __init__(self):
        pass

    async def find_all_agents(self):
        return await AgentDocument.all().to_list()

    async def find_agent_by_id(self, agent_id: PydanticObjectId):
        return await AgentDocument.get(agent_id)

    async def create(self, agent: Agent):
        agent_to_insert = AgentDocument(**agent.model_dump(by_alias=True))
        return await agent_to_insert.insert()


def get_agent_repository():
    return AgentRepository()


CommonAgentRepository = Annotated[
    AgentRepository, Depends(get_agent_repository, use_cache=True)
]
