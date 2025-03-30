from pydantic import BaseModel, Field


class ProcessEmbedQuery(BaseModel):
    embed_rules: bool = Field(default=False)
