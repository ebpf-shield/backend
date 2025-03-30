from typing import Optional
from pydantic import BaseModel, Field


class ProcessEmbedQuery(BaseModel):
    embed_rules: Optional[bool] = Field(alias="embedRules", default=False)
