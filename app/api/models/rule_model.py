import datetime
from enum import Enum
from typing import Literal, Optional

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, ConfigDict, Field, IPvAnyAddress

from app.core.utils.partial import partial_model

MIN_PORT_NUMBER = 0
MAX_PORT_NUMBER = 65535


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


class BaseRule(BaseModel):
    model_config = ConfigDict(
        validate_by_name=True,
        serialize_by_alias=True,
        validate_by_alias=True,
        extra="ignore",
    )

    id: Optional[PydanticObjectId] = Field(alias="_id", default=None)
    action: Optional[RuleAction] = Field(default=RuleAction.ACCEPT)
    protocol: Optional[RuleProtocol] = Field(default=RuleProtocol.TCP)
    priority: Optional[int] = Field(ge=0, le=100000, default=0)
    comment: Optional[str] = Field(max_length=255, default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="createdAt"
    )
    updated_at: datetime.datetime = Field(
        default_factory=datetime.datetime.now, alias="updatedAt"
    )
    process_id: PydanticObjectId = Field(alias="processId")
    # organization_id: PydanticObjectId = Field(alias="organizationId")


# TODO: Create input and output models for rules
class Rule(BaseRule):
    saddr: Optional[IPvAnyAddress] = Field(
        default=None, description="Source address (IP or CIDR)"
    )
    daddr: Optional[IPvAnyAddress] = Field(
        default=None, description="Destination address (IP or CIDR)"
    )
    daddr: Optional[IPvAnyAddress]
    sport: Optional[int] = Field(ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER, default=None)
    dport: Optional[int] = Field(ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER, default=None)
    chain: Optional[RuleChain] = Field(default=RuleChain.INPUT)


@partial_model()
class PartialRule(Rule):
    pass


class InputRule(BaseRule):
    saddr: IPvAnyAddress = Field(description="Source address (IP or CIDR)")
    sport: Optional[int] = Field(ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER, default=None)
    chain: Literal[RuleChain.INPUT] = Field(
        default=RuleChain.INPUT, description="Chain for the rule"
    )


@partial_model()
class PartialInputRule(InputRule):
    pass


class OutputRule(BaseRule):
    daddr: IPvAnyAddress = Field(description="Destination address (IP or CIDR)")
    dport: Optional[int] = Field(ge=MIN_PORT_NUMBER, le=MAX_PORT_NUMBER, default=None)
    chain: Literal[RuleChain.OUTPUT] = Field(
        default=RuleChain.OUTPUT, description="Chain for the rule"
    )


@partial_model()
class PartialOutputRule(OutputRule):
    pass


# TODO: Find a better name
type RuleBody = InputRule | OutputRule

type PartialRuleBody = PartialInputRule | PartialOutputRule


class RuleDocument(Document, Rule):
    pass

    class Settings:
        name = "rules"
        keep_nulls = False
