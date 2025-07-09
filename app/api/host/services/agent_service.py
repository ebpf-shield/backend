from typing import Annotated

import httpx
from beanie import PydanticObjectId
from fastapi import Depends

from app.api.host.repositories.agent_repository import (
    CommonHostAgentRepository,
    HostAgentRepository,
)
from app.api.models.agent_model import Agent, GeoLocationProperties
from app.core.config import settings


class HostAgentService:
    _agent_repository: HostAgentRepository

    def __init__(self, agent_repository: HostAgentRepository):
        self._agent_repository = agent_repository

    async def find_by_id(self, agent_id: PydanticObjectId):
        return await self._agent_repository.get_by_id(agent_id)

    async def create(self, agent: Agent):
        ip = agent.external_ip
        if not ip:
            return await self._agent_repository.create(agent)

        try:
            async with httpx.AsyncClient() as client:
                url = f"https://api.ip2location.io/?key={settings.GEO_IP_API_KEY}&ip={ip}&format=json"
                response = await client.get(url)

                response.raise_for_status()
                data = response.json()
                geo_data = GeoLocationProperties(**data)
                agent.geolocation_properties = geo_data

                return await self._agent_repository.create(agent)
        except httpx.HTTPError as e:
            raise e


def get_agent_service(agent_repository: CommonHostAgentRepository):
    return HostAgentService(agent_repository=agent_repository)


CommonHostAgentService = Annotated[
    HostAgentService, Depends(get_agent_service, use_cache=True)
]
