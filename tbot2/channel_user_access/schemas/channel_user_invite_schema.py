from datetime import datetime
from urllib.parse import urljoin
from uuid import UUID

from pydantic import computed_field

from tbot2.common import BaseRequestSchema, BaseSchema, TAccessLevel, datetime_now
from tbot2.config_settings import config


class ChannelUserInvite(BaseSchema):
    id: UUID
    channel_id: UUID
    access_level: TAccessLevel
    created_at: datetime
    expires_at: datetime

    @computed_field
    def is_expired(self) -> bool:
        return datetime_now() > self.expires_at

    @computed_field
    def invite_link(self) -> str:
        return urljoin(str(config.base_url), f'channel-invite/{self.id}')


class ChannelUserInviteCreate(BaseRequestSchema):
    access_level: TAccessLevel


class ChannelUserInviteUpdate(ChannelUserInviteCreate): ...
