from pydantic import BaseModel, Field


class AgentEmbedQuery(BaseModel):
    embed_processes: bool = Field(default=False)
