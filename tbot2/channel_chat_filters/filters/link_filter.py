from typing import Literal

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterLink(ChatFilterBase):
    type: Literal['link']


class ChatFilterLinkCreate(ChatFilterCreate):
    type: Literal['link']
    name: str = 'Link Filter'


class ChatFilterLinkUpdate(ChatFilterUpdate):
    type: Literal['link']
