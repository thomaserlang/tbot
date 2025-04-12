from uuid import UUID

from tbot2.common import TProvider
from tbot2.database import database


async def give_warning(
    *, channel_id: UUID, provider: TProvider, chatter_id: str, warning_duration: int
) -> None:
    await database.redis.set(
        f'tbot:warning:{channel_id}:{provider.value}:{chatter_id}',
        '1',
        ex=warning_duration,
    )


async def has_warning(
    *, channel_id: UUID, provider: TProvider, chatter_id: str
) -> bool:
    return await database.redis.exists(
        f'tbot:warning:{channel_id}:{provider.value}:{chatter_id}',
    )
