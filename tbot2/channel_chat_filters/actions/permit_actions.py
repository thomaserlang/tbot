from uuid import UUID

from tbot2.common import TProvider
from tbot2.database import database


async def create_permit(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
    seconds: int = 60,
) -> None:
    await database.redis.set(
        f'tbot:permit:{channel_id}:{provider.value}:{chatter_id}',
        '1',
        ex=seconds,
    )


async def has_permit(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
) -> bool:
    return await database.redis.exists(
        f'tbot:permit:{channel_id}:{provider.value}:{chatter_id}',
    )


async def delete_permit(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
) -> bool:
    return await database.redis.delete(
        f'tbot:permit:{channel_id}:{provider.value}:{chatter_id}',
    )
