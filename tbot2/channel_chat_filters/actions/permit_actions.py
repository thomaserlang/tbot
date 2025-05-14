from uuid import UUID

from tbot2.common import Provider
from tbot2.database import conn


async def create_permit(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    seconds: int = 60,
) -> None:
    await conn.redis.set(
        f'tbot:permit:{channel_id}:{provider}:{provider_viewer_id}',
        '1',
        ex=seconds,
    )


async def has_permit(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
) -> bool:
    return (
        await conn.redis.exists(
            f'tbot:permit:{channel_id}:{provider}:{provider_viewer_id}',
        )
    ) > 0


async def delete_permit(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
) -> bool:
    return (
        await conn.redis.delete(
            f'tbot:permit:{channel_id}:{provider}:{provider_viewer_id}',
        )
    ) > 0
