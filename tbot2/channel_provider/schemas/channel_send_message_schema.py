
from tbot2.common import BaseRequestSchema

from .channel_provider_schema import ChannelProvider


class SendChannelMessage(BaseRequestSchema):
    channel_provider: ChannelProvider
    message: str
