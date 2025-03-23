from typing import Literal

from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterCreate,
    ChatFilterUpdate,
)


class ChatFilterBannedTerms(ChatFilterBase):
    type: Literal['banned_terms']


class ChatFilterBannedTermsCreate(ChatFilterCreate):
    type: Literal['banned_terms']
    name: str = 'Banned Terms Filter'


class ChatFilterBannedTermsUpdate(ChatFilterUpdate):
    type: Literal['banned_terms']
