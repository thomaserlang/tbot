from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel


class EventSubSubscriptionTransport(BaseModel):
    method: str
    callback: str


class EventSubSubscription(BaseModel):
    id: str
    status: (
        Literal[
            'enabled',
            'webhook_callback_verification_pending',
            'webhook_callback_verification_failed',
            'notification_failures_exceeded',
            'authorization_revoked',
            'moderator_removed',
            'user_removed',
            'chat_user_banned',
            'version_removed',
            'beta_maintenance',
            'websocket_disconnected',
            'websocket_failed_ping_pong',
            'websocket_received_inbound_traffic',
            'websocket_connection_unused',
            'websocket_internal_error',
            'websocket_network_timeout',
            'websocket_network_error',
            'websocket_failed_to_reconnect',
        ]
        | str
    )
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
