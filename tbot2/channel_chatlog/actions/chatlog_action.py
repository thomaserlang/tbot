import sqlalchemy as sa

from tbot2.channel_viewer import ViewerNameHistoryRequest, save_viewers_name_history
from tbot2.common import ChatMessage
from tbot2.common.utils.json_utils import json_dumps
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import database

from ..models.chatlog_model import MChatlog


async def create_chatlog(
    data: ChatMessage,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> bool:
    data_ = data.model_dump()
    if 'access_level' in data_:
        data_.pop('access_level')  # do we wanna save this?
    async with get_session(session) as session:
        await session.execute(
            sa.insert(MChatlog.__table__).values(  # type: ignore
                **data_,
            )
        )

        await save_viewers_name_history(
            provider=data.provider,
            viewers=[
                ViewerNameHistoryRequest(
                    provider_viewer_id=data.provider_viewer_id,
                    name=data.viewer_name,
                    display_name=data.viewer_display_name,
                )
            ],
            session=session,
        )

    if publish:
        await database.redis.publish(
            f'tbot:live_chat:{data.channel_id}', json_dumps(data_)
        )
    return True
