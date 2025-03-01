import datetime
from enum import Enum
from typing import Optional

from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class Action(Enum, str):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"


class Chain(Enum, str):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class Protocol(Enum, str):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    ALL = "ALL"


class FirewallRule(BaseModel):
    saddr: Optional[str]
    daddr: Optional[str]
    sport: int
    dport: int
    protocol: Optional[str]
    action: Optional[Action] = Action.ACCEPT
    chain: Optional[str] = Chain.INPUT
    priority: int = 0
    command: str
    comment: Optional[str]
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.now)
    agent_guid: PydanticObjectId
