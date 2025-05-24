from datetime import datetime
from typing import Annotated, Literal
from uuid import UUID

from pydantic import StringConstraints, computed_field
from typing_extensions import Doc

from ..types.chat_message_type import ChatMessageType
from ..types.provider_type import Provider
from .base_schema import BaseSchema
from .chat_message_request_schemas import ChatMessagePartRequest
from .image_urls_schema import ImageUrls


class ChatMessageBadge(BaseSchema):
    id: str
    type: str
    name: str


class EmotePart(BaseSchema):
    id: str
    name: str
    animated: bool
    emote_provider: str

    @computed_field  # type: ignore[misc]
    @property
    def urls(self) -> ImageUrls | None:
        match self.emote_provider:
            case 'twitch':
                return ImageUrls(
                    sm=f'https://static-cdn.jtvnw.net/emoticons/v2/{self.id}/default/dark/1.0',
                    md=f'https://static-cdn.jtvnw.net/emoticons/v2/{self.id}/default/dark/2.0',
                    lg=f'https://static-cdn.jtvnw.net/emoticons/v2/{self.id}/default/dark/3.0',
                )
            case '7tv':
                return ImageUrls(
                    sm=f'https://cdn.7tv.app/emote/{self.id}/1x.webp',
                    md=f'https://cdn.7tv.app/emote/{self.id}/2x.webp',
                    lg=f'https://cdn.7tv.app/emote/{self.id}/3x.webp',
                )
            case 'bttv':
                return ImageUrls(
                    sm=f'https://cdn.betterttv.net/emote/{self.id}/1x.webp',
                    md=f'https://cdn.betterttv.net/emote/{self.id}/2x.webp',
                    lg=f'https://cdn.betterttv.net/emote/{self.id}/3x.webp',
                )
            case _:
                return None


class MentionPart(BaseSchema):
    user_id: str
    username: str
    display_name: str


class GiftPart(BaseSchema):
    id: str
    name: str
    type: str
    count: int
    animated: bool = False


class ChatMessagePart(BaseSchema):
    type: Literal['text', 'emote', 'mention', 'gift']
    text: str
    gift: GiftPart | None = None
    emote: EmotePart | None = None
    mention: MentionPart | None = None


class ChatMessage(BaseSchema):
    id: UUID
    type: ChatMessageType
    sub_type: Annotated[str, StringConstraints(min_length=1, max_length=100)] | None = (
        None
    )
    created_at: datetime
    channel_id: Annotated[UUID, Doc('The ID of the TBot channel')]
    provider: Provider
    provider_channel_id: str
    provider_message_id: str
    provider_viewer_id: str
    viewer_name: str
    viewer_display_name: str
    viewer_color: Annotated[str, Doc('Hex color')] | None = None
    message: str
    message_parts: list[ChatMessagePart] = []
    badges: list[ChatMessageBadge] = []
    notice_message: str = ''
    notice_message_parts: list[ChatMessagePart] = []

    def message_without_parts(self) -> str:
        if not self.message_parts:
            return self.message
        return ''.join(
            parts.text for parts in self.message_parts if parts.type == 'text'
        )

    def parts_to_request(self) -> list[ChatMessagePartRequest]:
        return [
            ChatMessagePartRequest.model_validate(part) for part in self.message_parts
        ]
