from datetime import datetime
from typing import Annotated, Literal

from pydantic import Field

from tbot2.common import BaseSchema
from tbot2.common.types.chat_message_type import TwitchModerateAction


class ModerateMetadataFollowers(BaseSchema):
    follow_duration_minutes: int


class ModerateUserBase(BaseSchema):
    user_id: str
    user_login: str
    user_name: str


class ModerateMetadataSlow(BaseSchema):
    wait_time_seconds: int


class ModerateMetadataVip(ModerateUserBase): ...


class ModerateMetadataUnvip(ModerateUserBase): ...


class ModerateMetadataMod(ModerateUserBase): ...


class ModerateMetadataUnmod(ModerateUserBase): ...


class ModerateMetadataBan(ModerateUserBase):
    reason: str | None


class ModerateMetadataUnban(ModerateUserBase): ...


class ModerateMetadataTimeout(ModerateUserBase):
    reason: str
    expires_at: datetime


class ModerateMetadataUntimeout(ModerateUserBase): ...


class ModerateMetadataRaid(ModerateUserBase):
    viewer_count: int


class ModerateMetadataUnraid(ModerateUserBase): ...


class ModerateMetadataEmoteOnly(ModerateUserBase):
    message_id: str
    message_body: str


class ModerateMetadataAutomodTerms(BaseSchema):
    action: str | Literal['add', 'remove']
    action_list: Annotated[str | Literal['blocked', 'permitted'], Field(alias='list')]
    terms: list[str]
    from_automod: bool


class ModerateMetadataUnbanRequest(ModerateUserBase):
    is_approved: bool
    moderator_message: str


class ModerateMetadataWarn(ModerateUserBase):
    reason: str | None = None
    chat_rultes_cited: list[str] | None = None


class ModerateMetadataDelete(ModerateUserBase):
    message_id: str
    message_body: str


class EventChannelModerate(BaseSchema):
    broadcaster_user_id: str
    broadcaster_user_login: str
    broadcaster_user_name: str
    source_broadcaster_user_id: str | None
    source_broadcaster_user_login: str | None
    source_broadcaster_user_name: str | None
    moderator_user_id: str
    moderator_user_login: str
    moderator_user_name: str
    action: str | TwitchModerateAction
    followers: ModerateMetadataFollowers | None = None
    slow: ModerateMetadataSlow | None = None
    vip: ModerateMetadataVip | None = None
    unvip: ModerateMetadataUnvip | None = None
    warn: ModerateMetadataWarn | None = None
    mod: ModerateMetadataMod | None = None
    unmod: ModerateMetadataUnmod | None = None
    ban: ModerateMetadataBan | None = None
    unban: ModerateMetadataUnban | None = None
    timeout: ModerateMetadataTimeout | None = None
    untimeout: ModerateMetadataUntimeout | None = None
    raid: ModerateMetadataRaid | None = None
    unraid: ModerateMetadataUnraid | None = None
    delete: ModerateMetadataDelete | None = None
    automod_terms: ModerateMetadataAutomodTerms | None = None
    unban_request: ModerateMetadataUnbanRequest | None = None
