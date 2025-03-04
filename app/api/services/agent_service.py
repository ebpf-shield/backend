from typing import Annotated

from fastapi import Depends


class AgentService:
    def __init__(self):
        pass


def get_agent_service():
    return AgentService()


CommonAgentService = Annotated[AgentService, Depends(get_agent_service, use_cache=True)]
