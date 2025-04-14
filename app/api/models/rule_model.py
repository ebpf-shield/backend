import datetime
from enum import Enum
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field, IPvAnyAddress


class RuleAction(str, Enum):
    ACCEPT = "ACCEPT"
    DROP = "DROP"
    REJECT = "REJECT"


class RuleChain(str, Enum):
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"


class RuleProtocol(str, Enum):
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"


class Rule(BaseModel):
    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    saddr: Optional[IPvAnyAddress]
    daddr: Optional[IPvAnyAddress]
    sport: int = Field(ge=0, le=65535)
    dport: int = Field(ge=0, le=65535)
    protocol: Optional[RuleProtocol] = Field(default=RuleProtocol.TCP)
    action: Optional[RuleAction] = Field(default=RuleAction.ACCEPT)
    chain: Optional[RuleChain] = Field(default=RuleChain.INPUT)
    priority: int = Field(ge=0, le=100000)
    comment: Optional[str] = Field(max_length=255)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="createdAt"
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="updatedAt"
    )
    process_id: PydanticObjectId = Field(alias="processId")


class RuleDocument(Document, Rule):
    pass

    class Settings:
        name = "rules"
