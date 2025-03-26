import shlex
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
)
from ..types import TBannedTermType


class ChatFilterBannedTermsCreate(ChatFilterBaseCreate):
    type: Literal['banned_terms']
    name: str = 'Banned Terms Filter'


class ChatFilterBannedTermsUpdate(ChatFilterBaseUpdate):
    type: Literal['banned_terms']


class ChatFilterBannedTerms(ChatFilterBase):
    type: Literal['banned_terms']

    async def check_message(self, message: ChatMessage) -> bool:
        banned_terms = await get_banned_terms(filter_id=self.id)
        for term in banned_terms:
            if (term.type == TBannedTermType.re) or (
                term.text.startswith('re:')  # Backwards compatibility
            ):
                if search(
                    term.text if not term.text.startswith('re:') else term.text[3:],
                    message.message_without_fragments(),
                    flags=IGNORECASE,
                ):
                    return True
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
                    return True
        return False


@alru_cache(ttl=1)
async def get_banned_terms(filter_id: UUID):
    return await _get_banned_terms(filter_id=filter_id)
