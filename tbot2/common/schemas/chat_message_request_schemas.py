from datetime import datetime
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import (
    Field,
    StringConstraints,
    ValidationInfo,
    field_validator,
    model_validator,
)
from typing_extensions import Doc
from uuid6 import uuid7

from ..types.access_level_type import TAccessLevel
from ..types.chat_message_type import ChatMessageSubType, ChatMessageType
from ..types.provider_type import Provider
from ..utils.datetime_now import datetime_now
from ..utils.username_color_generate import username_color_generator
from .base_request_schema import BaseRequestSchema


class ChatMessageBadgeRequest(BaseRequestSchema):
    id: str
    type: str
    name: str


class EmotePartRequest(BaseRequestSchema):
    id: str
    name: str
    animated: bool
    emote_provider: str


class MentionPartRequest(BaseRequestSchema):
    user_id: str
    username: str
    display_name: str


GiftPartType = Literal['cheermote']


class GiftPartRequest(BaseRequestSchema):
    id: str
    name: str
    type: str | GiftPartType
    count: int
    animated: bool = False


class ChatMessagePartRequest(BaseRequestSchema):
    type: Literal['text', 'emote', 'mention', 'gift']
    text: str
    gift: GiftPartRequest | None = None
    emote: EmotePartRequest | None = None
    mention: MentionPartRequest | None = None


class ChatMessageCreate(BaseRequestSchema):
    id: UUID = Field(default_factory=uuid7)
    type: ChatMessageType
    sub_type: (
        Annotated[
            ChatMessageSubType | str, StringConstraints(min_length=1, max_length=100)
        ]
        | None
    ) = None
    created_at: datetime = Field(default_factory=datetime_now)
    channel_id: Annotated[UUID, Doc('The ID of the TBot channel')]
    provider: Provider
    provider_channel_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
    provider_message_id: Annotated[str, StringConstraints(min_length=1, max_length=255)]
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
    ) = Field(
        default_factory=lambda data: username_color_generator(data['viewer_name'])
    )
    message: Annotated[str, StringConstraints(min_length=0, max_length=2000)] = ''
    message_parts: list[ChatMessagePartRequest] = Field(
        default_factory=lambda data: [
            ChatMessagePartRequest(
                type='text',
                text=data['message'],
            )
        ]
        if data['message']
        else []
    )
    badges: list[ChatMessageBadgeRequest] = []
    access_level: TAccessLevel = TAccessLevel.PUBLIC
    notice_message: Annotated[str, StringConstraints(min_length=0, max_length=500)] = ''
    notice_message_parts: list[ChatMessagePartRequest] | None = Field(
        default_factory=lambda data: [
            ChatMessagePartRequest(
                type='text',
                text=data['notice_message'],
            )
        ]
        if data['notice_message']
        else []
    )

    @field_validator('viewer_color', mode='before')
    @classmethod
    def viewer_color_not_empty(cls, value: str | None) -> str | None:
        if not value:
            return None
        return value

    @field_validator('viewer_color', mode='after')
    @classmethod
    def viewer_color_set(cls, value: str | None, info: ValidationInfo) -> str:
        if not value:
            return username_color_generator(info.data['viewer_name'])
        return value

    @model_validator(mode='after')
    def message_default(self) -> Self:
        if self.notice_message and not self.notice_message_parts:
            self.notice_message_parts = [
                ChatMessagePartRequest(
                    type='text',
                    text=self.notice_message,
                )
            ]
        if self.message and not self.message_parts:
            self.message_parts = [
                ChatMessagePartRequest(
                    type='text',
                    text=self.message,
                )
            ]
        return self

    def message_without_parts(self) -> str:
        if not self.message_parts:
            return self.message
        return ''.join(
            parts.text for parts in self.message_parts if parts.type == 'text'
        )
