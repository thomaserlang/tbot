
from tbot2.common import BaseRequestSchema

from ..schemas.channel_oauth_provider_schema import ChannelOAuthProvider


class SendChannelMessage(BaseRequestSchema):
    channel_provider: ChannelOAuthProvider
    message: str
