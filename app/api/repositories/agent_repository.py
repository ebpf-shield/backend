from typing import Annotated

from beanie import PydanticObjectId
from beanie.operators import Set
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

    async def update_rules(
        self, agent_id: PydanticObjectId, rules: list[PydanticObjectId]
    ):
        return await AgentDocument.find_one({AgentDocument._id: agent_id}).update_one(
            Set({AgentDocument.rules: rules})
        )


def get_agent_repository():
    return AgentRepository()


CommonAgentRepository = Annotated[
    AgentRepository, Depends(get_agent_repository, use_cache=True)
]
