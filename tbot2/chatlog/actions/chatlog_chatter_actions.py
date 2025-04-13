import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert

from tbot2.common import TProvider, datetime_now
from tbot2.contexts import AsyncSession, get_session

from ..models.chatlog_chatters_model import MChatlogChatters
from ..schemas.chatlog_chatter_schema import ChatterRequest


async def save_chatters(
    provider: TProvider,
    chatters: list[ChatterRequest],
    session: AsyncSession | None = None,
) -> None:
    last_seen_at = datetime_now()
    async with get_session(session) as session:
        await session.execute(
            insert(MChatlogChatters.__table__)  # type: ignore
            .values(
                [
                    {
                        'provider': provider,
                        'chatter_id': chatter.chatter_id,
                        'chatter_name': chatter.chatter_name,
                        'chatter_display_name': chatter.chatter_display_name,
                        'last_seen_at': last_seen_at,
                    }
                    for chatter in chatters
                ]
            )
            .on_duplicate_key_update(
                chatter_name=sa.func.values(MChatlogChatters.chatter_name),
                chatter_display_name=sa.func.values(
                    MChatlogChatters.chatter_display_name
                ),
                last_seen_at=sa.func.values(MChatlogChatters.last_seen_at),
            )
        )
