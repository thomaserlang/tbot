from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel


class EventSubSubscription(BaseModel):
    id: str
    status: str
    type: str
    version: str
    created_at: datetime


TypeEvent = TypeVar('TypeEvent')


class EventSubNotification(BaseModel, Generic[TypeEvent]):
    subscription: EventSubSubscription
    event: TypeEvent
