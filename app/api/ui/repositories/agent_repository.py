from typing import Annotated

from beanie import PydanticObjectId
from fastapi import Depends

from app.api.models.agent_model import Agent, AgentDocument, AgentWithProcesses


class UIAgentRepository:
    def __init__(self):
        pass

    async def get_all(self, organization_id: PydanticObjectId):
        return await AgentDocument.find(
            {Agent.organization_id: organization_id}
        ).to_list()

    async def get_all_with_processes(self, organization_id: PydanticObjectId):
        return await AgentDocument.aggregate(
            [
                {"$match": {"organizationId": organization_id}},
                {
                    "$lookup": {
                        "from": "processes",
                        "localField": "_id",
                        "foreignField": "agentId",
                        "as": "processes",
                    }
                },
            ],
            projection_model=AgentWithProcesses,
        ).to_list()

    async def get_by_id(self, agent_id: PydanticObjectId):
        return await AgentDocument.get(agent_id)

    async def get_by_id_with_processes(self, agent_id: PydanticObjectId):
        [agent] = await AgentDocument.aggregate(
            [
                {"$match": {"_id": agent_id}},
                {
                    "$lookup": {
                        "from": "processes",
                        "localField": "_id",
                        "foreignField": "agentId",
                        "as": "processes",
                    }
                },
            ],
            projection_model=AgentWithProcesses,
        ).to_list()

        return agent

    async def create(self, agent: Agent):
        agent_to_insert = AgentDocument(**agent.model_dump(by_alias=True))
        return await agent_to_insert.insert()

    async def update(self, agent: Agent):
        agent_to_update = AgentDocument(**agent.model_dump(by_alias=True))
        return await agent_to_update.update()


def get_agent_repository():
    return UIAgentRepository()


CommonUIAgentRepository = Annotated[
    UIAgentRepository, Depends(get_agent_repository, use_cache=True)
]
