import sys
from uuid import UUID

from async_lru import alru_cache

from tbot2.common import ChatMessage

from ..schemas.chat_filter_schema import FilterMatchResult
from .chat_filter_actions import get_chat_filters as _get_chat_filters
from .permit_actions import has_permit


async def matches_filter(chat_message: ChatMessage) -> FilterMatchResult | None:
    filters = await get_channel_filters(chat_message.channel_id)
    for filter in filters:
        if chat_message.access_level >= filter.exclude_access_level:
            continue
        result = await filter.check_message(chat_message)
        if result.matched:
            if await has_permit(
                channel_id=chat_message.channel_id,
                provider=chat_message.provider,
                chatter_id=chat_message.chatter_id,
            ):
                return None
            return result


@alru_cache(ttl=1, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_channel_filters(channel_id: UUID):
    return await _get_chat_filters(channel_id)
