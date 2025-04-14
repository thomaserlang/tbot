from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import StringConstraints
from typing_extensions import Doc

from tbot2.common import BaseRequestSchema

from ..types.access_level_type import TAccessLevel
from ..types.provider_type import Provider
from .twitch_schemas import TwitchBadge, TwitchMessageFragment


class ChatMessage(BaseRequestSchema):
    type: Literal['message', 'notice', 'mod_action']
    sub_type: Annotated[str, StringConstraints(min_length=1, max_length=100)] | None = (
        None
    )
    created_at: datetime
    provider: Provider
    provider_id: Annotated[str, StringConstraints(min_length=1, max_length=36)]
    channel_id: Annotated[UUID, Doc('The ID of the TBot channel')]
    chatter_id: Annotated[str, StringConstraints(min_length=1, max_length=36)]
    chatter_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    chatter_display_name: Annotated[
        str, StringConstraints(min_length=1, max_length=200)
    ]
    chatter_color: (
        Annotated[
            str,
            StringConstraints(
                min_length=4, max_length=7, pattern='^#[0-9A-Fa-f]{3,6}$'
            ),
        ]
        | None
    ) = None
    message: Annotated[str, StringConstraints(min_length=1, max_length=600)]
    msg_id: Annotated[str, StringConstraints(min_length=1, max_length=36)]
    twitch_badges: list[TwitchBadge] | None = None
    twitch_fragments: list[TwitchMessageFragment] | None = None

    def message_without_fragments(self) -> str:
        if not self.twitch_fragments:
            return self.message
        return ''.join(
            fragment.text
            for fragment in self.twitch_fragments
            if fragment.type == 'text'
        )

    @property
    def access_level(self) -> TAccessLevel:
        if self.twitch_badges:
            for badge in self.twitch_badges:
                match badge.set_id:
                    case 'moderator':
                        return TAccessLevel.MOD
                    case 'broadcaster':
                        return TAccessLevel.OWNER
                    case 'vip':
                        return TAccessLevel.VIP
                    case _:
                        return TAccessLevel.PUBLIC
        return TAccessLevel.PUBLIC
