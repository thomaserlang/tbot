from uuid import UUID

from tbot2.common import BaseSchema


class ChannelUserAccessLevel(BaseSchema):
    user_id: UUID
    channel_id: UUID
    access_level: int
