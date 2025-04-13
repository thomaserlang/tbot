from typing import Literal
from uuid import UUID

from tbot2.common import BaseRequestSchema, TProvider


class SendChannelMessage(BaseRequestSchema):
    channel_id: UUID
    provider: TProvider | Literal['all']
    message: str
