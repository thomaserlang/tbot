from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel


class EventSubSubscriptionTransport(BaseModel):
    method: str
    callback: str


class EventSubSubscription(BaseModel):
    id: str
    status: str
    type: str
    version: str
    created_at: datetime
    condition: dict[str, str]
    transport: EventSubSubscriptionTransport


class EventSubRegistration(BaseModel):
    event_type: str
    version: str
    condition: dict[str, str]


TypeEvent = TypeVar('TypeEvent')


class EventSubNotification(BaseModel, Generic[TypeEvent]):
    subscription: EventSubSubscription
    event: TypeEvent
