import sys
from uuid import UUID

from async_lru import alru_cache

from tbot2.channel_chat_filters.actions.warning_actions import give_warning, has_warning
from tbot2.common import ChatMessage

from ..schemas.chat_filter_schema import FilterMatchResult
from .chat_filter_actions import ChatFilterBase, get_chat_filters
from .permit_actions import has_permit


async def matches_filter(chat_message: ChatMessage) -> FilterMatchResult | None:
    filters = await get_channel_filters_cached(chat_message.channel_id)
    for filter in filters:
        if chat_message.access_level >= filter.exclude_access_level:
            continue
        result = await filter.check_message(chat_message)
        if not result.matched:
            continue

        if await has_permit(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=chat_message.chatter_id,
        ):
            return None

        result.action = 'timeout'

        if filter.warning_enabled and not await has_warning(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=chat_message.chatter_id,
        ):
            result.action = 'warning'
            await give_warning(
                channel_id=chat_message.channel_id,
                provider=chat_message.provider,
                chatter_id=chat_message.chatter_id,
                warning_duration=filter.warning_expire_duration,
            )

        return result


@alru_cache(ttl=1, maxsize=1000 if 'pytest' not in sys.modules else 0)
async def get_channel_filters_cached(channel_id: UUID) -> list[ChatFilterBase]:
    return await get_chat_filters(channel_id)
