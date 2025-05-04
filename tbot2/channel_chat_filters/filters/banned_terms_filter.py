import sys
from re import IGNORECASE, search
from typing import Literal
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessageRequest, check_pattern_match

from ..actions.banned_term_actions import BannedTerm, get_banned_terms
from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseUpdate,
    ChatFilterName,
    ChatFilterTimeoutMessage,
    ChatFilterWarningMessage,
    FilterMatchResult,
)


class ChatFilterBannedTermsCreate(ChatFilterBaseCreate):
    type: Literal['banned_terms']
    name: ChatFilterName = 'Banned Terms Filter'
    warning_message: ChatFilterWarningMessage = 'Banned word'
    timeout_message: ChatFilterTimeoutMessage = 'Banned word'


class ChatFilterBannedTermsUpdate(ChatFilterBaseUpdate):
    type: Literal['banned_terms']


class ChatFilterBannedTerms(ChatFilterBase):
    type: Literal['banned_terms']

    async def check_message(self, message: ChatMessageRequest) -> FilterMatchResult:
        banned_terms = await get_banned_terms_cached(filter_id=self.id)
        for term in banned_terms:
            if term.type == 'regex':
                if search(
                    term.text if not term.text.startswith('re:') else term.text[3:],
                    message.message_without_parts(),
                    flags=IGNORECASE,
                ):
                    return FilterMatchResult(filter=self, matched=True, sub_id=term.id)
            elif term.type == 'phrase':
                if check_pattern_match(
                    message=message.message_without_parts(),
                    pattern=term.text,
                    normalize=True,
                    strip_symbols=True,
                    collaps_letters=True,
                    check_leetspeak=True,
                ):
                    return FilterMatchResult(filter=self, matched=True, sub_id=term.id)
        return FilterMatchResult(filter=self, matched=False)


@alru_cache(ttl=1, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_banned_terms_cached(filter_id: UUID) -> list[BannedTerm]:
    return await get_banned_terms(filter_id=filter_id)
