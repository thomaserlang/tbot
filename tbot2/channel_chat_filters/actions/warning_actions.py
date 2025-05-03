from uuid import UUID

from tbot2.common import Provider
from tbot2.database import database


async def give_warning(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    warning_duration: int,
) -> None:
    await database.redis.set(
        f'tbot:warning:{channel_id}:{provider}:{provider_viewer_id}',
        '1',
        ex=warning_duration,
    )


async def has_warning(
    *, channel_id: UUID, provider: Provider, provider_viewer_id: str
) -> bool:
    return await database.redis.exists(
        f'tbot:warning:{channel_id}:{provider}:{provider_viewer_id}',
    )
