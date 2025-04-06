import shlex
import sys
from re import IGNORECASE, search
from typing import Literal
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessage

from ..actions.banned_term_actions import get_banned_terms as _get_banned_terms
from ..schemas.chat_filter_schema import (
    ChatFilterBase,
    ChatFilterBaseCreate,
    ChatFilterBaseUpdate,
    ChatFilterName,
    ChatFilterTimeoutMessage,
    ChatFilterWarningMessage,
    FilterMatchResult,
)
from ..types import TBannedTermType


class ChatFilterBannedTermsCreate(ChatFilterBaseCreate):
    type: Literal['banned_terms']
    name: ChatFilterName = 'Banned Terms Filter'
    warning_message: ChatFilterWarningMessage = 'Banned word [warning]'
    timeout_message: ChatFilterTimeoutMessage = 'Banned word'


class ChatFilterBannedTermsUpdate(ChatFilterBaseUpdate):
    type: Literal['banned_terms']


class ChatFilterBannedTerms(ChatFilterBase):
    type: Literal['banned_terms']

    async def check_message(self, message: ChatMessage) -> FilterMatchResult:
        banned_terms = await get_banned_terms(filter_id=self.id)
        for term in banned_terms:
            if (term.type == TBannedTermType.regex) or (
                term.text.startswith('re:')  # Backwards compatibility
            ):
                if search(
                    term.text if not term.text.startswith('re:') else term.text[3:],
                    message.message_without_fragments(),
                    flags=IGNORECASE,
                ):
                    return FilterMatchResult(filter=self, matched=True, sub_id=term.id)
            elif term.type == TBannedTermType.phrase:
                split = (
                    term.text.split(' ')
                    if '"' not in term.text
                    else shlex.split(term.text)
                )
                if all(
                    [
                        search(
                            rf'\b{s}\b',
                            message.message_without_fragments(),
                            flags=IGNORECASE,
                        )
                        for s in split
                    ]
                ):
                    return FilterMatchResult(filter=self, matched=True, sub_id=term.id)
        return FilterMatchResult(filter=self, matched=False)


@alru_cache(ttl=1, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_banned_terms(filter_id: UUID):
    return await _get_banned_terms(filter_id=filter_id)
