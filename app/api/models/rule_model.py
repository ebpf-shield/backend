import datetime
from enum import Enum
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field


class Action(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"


class Chain(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class Protocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ALL = "ALL"


class FirewallRule(BaseModel):
    saddr: Optional[str]
    daddr: Optional[str]
    sport: int = Field(ge=0, le=65535)
    dport: int = Field(ge=0, le=65535)
    protocol: Optional[str]
    action: Optional[Action] = Field(default=Action.ACCEPT)
    chain: Optional[Chain] = Field(default=Chain.INPUT)
    priority: int = Field(ge=0, le=100000)
    command: str = Field(max_length=255)
    comment: Optional[str]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    agent_id: PydanticObjectId


class FirewallRuleDocument(Document, FirewallRule):
    pass

    class Settings:
        name = "rules"
