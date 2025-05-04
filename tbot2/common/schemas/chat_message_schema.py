from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import StringConstraints, field_validator
from typing_extensions import Doc

from tbot2.common import BaseRequestSchema

from ..types.access_level_type import TAccessLevel
from ..types.provider_type import Provider

ChatMessageType = Literal['message', 'notice', 'mod_action']


class ChatMessageBadge(BaseRequestSchema):
    id: str
    type: str
    name: str


class EmotePart(BaseRequestSchema):
    id: str
    name: str
    animated: bool
    emote_provider: str


class MentionPart(BaseRequestSchema):
    user_id: str
    username: str
    display_name: str


class GiftPart(BaseRequestSchema):
    id: str
    name: str
    type: str
    count: int


class ChatMessagePart(BaseRequestSchema):
    type: Literal['text', 'emote', 'mention', 'gift']
    text: str
    gift: GiftPart | None = None
    emote: EmotePart | None = None
    mention: MentionPart | None = None


class ChatMessage(BaseRequestSchema):
    id: UUID
    type: ChatMessageType
    sub_type: Annotated[str, StringConstraints(min_length=1, max_length=100)] | None = (
        None
    )
    created_at: datetime
    provider: Provider
    provider_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    channel_id: Annotated[UUID, Doc('The ID of the TBot channel')]
    provider_viewer_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    viewer_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    viewer_display_name: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    viewer_color: (
        Annotated[
            str,
            StringConstraints(
                min_length=4, max_length=7, pattern='^#[0-9A-Fa-f]{3,6}$'
            ),
        ]
        | None
    ) = None
    message: Annotated[str, StringConstraints(min_length=1, max_length=2000)]
    msg_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    badges: list[ChatMessageBadge] = []
    parts: list[ChatMessagePart] = []
    access_level: TAccessLevel = TAccessLevel.PUBLIC

    @field_validator('viewer_color', mode='before')
    @classmethod
    def validate_viewer_color(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value

    def message_without_parts(self) -> str:
        if not self.parts:
            return self.message
        return ''.join(parts.text for parts in self.parts if parts.type == 'text')
