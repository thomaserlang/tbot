from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, StringConstraints, ValidationInfo, field_validator
from typing_extensions import Doc
from uuid6 import uuid7

from tbot2.common import BaseRequestSchema
from tbot2.common.utils.username_color_generate import username_color_generator

from ..types.access_level_type import TAccessLevel
from ..types.chat_message_type import ChatMessageType
from ..types.provider_type import Provider


class ChatMessageBadgeRequest(BaseRequestSchema):
    id: str
    type: str
    info: str


class EmotePartRequest(BaseRequestSchema):
    id: str
    name: str
    animated: bool
    emote_provider: str


class MentionPartRequest(BaseRequestSchema):
    user_id: str
    username: str
    display_name: str


class GiftPartRequest(BaseRequestSchema):
    id: str
    name: str
    type: str
    count: int
    animated: bool = False


class ChatMessagePartRequest(BaseRequestSchema):
    type: Literal['text', 'emote', 'mention', 'gift']
    text: str
    gift: GiftPartRequest | None = None
    emote: EmotePartRequest | None = None
    mention: MentionPartRequest | None = None


class ChatMessageRequest(BaseRequestSchema):
    id: Annotated[UUID, Field(default_factory=uuid7)]
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
    badges: list[ChatMessageBadgeRequest] = []
    parts: list[ChatMessagePartRequest] = []
    access_level: TAccessLevel = TAccessLevel.PUBLIC

    @field_validator('viewer_color', mode='before')
    @classmethod
    def viewer_color_not_empty(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value

    @field_validator('viewer_color', mode='after')
    @classmethod
    def viewer_color_generate(cls, value: str | None, info: ValidationInfo) -> str:
        if not value:
            return username_color_generator(info.data['viewer_name'])
        return value

    def message_without_parts(self) -> str:
        if not self.parts:
            return self.message
        return ''.join(parts.text for parts in self.parts if parts.type == 'text')
