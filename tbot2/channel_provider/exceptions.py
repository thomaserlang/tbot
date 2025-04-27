from uuid import UUID

from tbot2.common import Provider
from tbot2.common.exceptions import ErrorMessage
from tbot2.config_settings import config


class ChannelProviderOAuthNotFound(ErrorMessage):
    def __init__(self, channel_id: UUID, provider: Provider) -> None:
        super().__init__(
            f'{provider} must be added as a provider: '
            f'{config.base_url}channels/{channel_id}/providers'
        )
        self.channel_id = channel_id
        self.provider = provider
