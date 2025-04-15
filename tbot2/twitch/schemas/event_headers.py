from dataclasses import dataclass
from datetime import datetime
from typing import Annotated

from fastapi import Header


@dataclass
class EventSubHeaders:
    message_id: Annotated[str, Header(alias='Twitch-Eventsub-Message-Id')]
    message_type: Annotated[str, Header(alias='Twitch-Eventsub-Message-Type')]
    message_timestamp_raw: Annotated[
        str, Header(alias='Twitch-Eventsub-Message-Timestamp')
    ]
    message_timestamp: Annotated[
        datetime, Header(alias='Twitch-Eventsub-Message-Timestamp')
    ]
    message_signature: Annotated[str, Header(alias='Twitch-Eventsub-Message-Signature')]
