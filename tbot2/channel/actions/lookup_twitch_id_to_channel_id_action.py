from uuid import UUID

import sqlalchemy as sa

from tbot2.contexts import get_session
from tbot2.database import database

from ..models.channel_model import MChannel


async def lookup_twitch_id_to_channel_id(twitch_id: str):
    user_id = await database.redis.get(f'tbot:twitch_id_to_channel_id:{twitch_id}')
    if user_id:
        return UUID(user_id)
    async with get_session() as session:
        user_id = await session.scalar(
            sa.select(MChannel.id).where(MChannel.twitch_id == twitch_id)
        )
        if user_id:
            return
        await database.redis.set(
            f'tbot:twitch_id_to_channel_id:{twitch_id}', str(user_id), ex=60 * 60 * 24
        )
        return user_id


async def clear_twitch_id_to_user_id_cache(twitch_id: str):
    await database.redis.delete(f'tbot:twitch_id_to_channel_id:{twitch_id}')
