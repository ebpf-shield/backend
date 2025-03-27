import datetime
from enum import Enum
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, IPvAnyAddress


class Action(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"


class Chain(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class Rule(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id")
    saddr: Optional[IPvAnyAddress]
    daddr: Optional[IPvAnyAddress]
    sport: int = Field(ge=0, le=65535)
    dport: int = Field(ge=0, le=65535)
    protocol: Optional[str]
    action: Optional[Action] = Field(default=Action.ACCEPT)
    chain: Optional[Chain] = Field(default=Chain.INPUT)
    priority: int = Field(ge=0, le=100000)
    comment: Optional[str] = Field(max_length=255)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="createdAt"
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="updatedAt"
    )
    process_id: PydanticObjectId


class RuleDocument(Document, Rule):
    pass

    class Settings:
        name = "rules"
