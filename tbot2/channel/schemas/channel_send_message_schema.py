from typing import Literal
from uuid import UUID

from tbot2.common import BaseRequestSchema, Provider


class SendChannelMessage(BaseRequestSchema):
    channel_id: UUID
    provider: Provider | Literal['all']
    message: str
