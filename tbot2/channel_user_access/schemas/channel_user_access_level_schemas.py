from uuid import UUID

from tbot2.common import BaseSchema, TAccessLevel
from tbot2.user import User


class ChannelUserAccessLevel(BaseSchema):
    id: UUID
    user_id: UUID
    channel_id: UUID
    access_level: TAccessLevel


class ChannelUserAccessLevelWithUser(BaseSchema):
    id: UUID
    user: User
    channel_id: UUID
    access_level: TAccessLevel
