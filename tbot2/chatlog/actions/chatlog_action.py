
import sqlalchemy as sa
from sqlalchemy.dialects.mysql import insert

from tbot2.common.schemas.chat_message_schema import ChatMessage
from tbot2.contexts import AsyncSession, get_session

from ..actions.chatlog_chatter_actions import save_chatters
from ..models.chatlog_chatter_stats_model import MChatlogChatterStats
from ..models.chatlog_model import MChatlog
from ..schemas.chatlog_chatter_schema import ChatterRequest


async def create_chatlog(
    data: ChatMessage,
    session: AsyncSession | None = None,
) -> bool:
    async with get_session(session) as session:
        await session.execute(
            sa.insert(MChatlog.__table__).values(  # type: ignore
                **data.model_dump(),
            )
        )

        await session.execute(
            insert(MChatlogChatterStats.__table__)  # type: ignore
            .values(
                channel_id=data.channel_id,
                provider=data.provider,
                chatter_id=data.chatter_id,
                chat_messages=1,
            )
            .on_duplicate_key_update(
                chat_messages=MChatlogChatterStats.chat_messages + 1
            )
        )

        await save_chatters(
            provider=data.provider,
            chatters=[
                ChatterRequest(
                    chatter_id=data.chatter_id,
                    chatter_name=data.chatter_name,
                    chatter_display_name=data.chatter_display_name,
                )
            ],
            session=session,
        )

    return True
