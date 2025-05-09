import sqlalchemy as sa
from loguru import logger

from tbot2.channel_viewer import ViewerNameHistoryRequest, save_viewers_name_history
from tbot2.common import ChatMessage, ChatMessagePartRequest, ChatMessageRequest
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import database

from ..models.chatlog_model import MChatlog


async def create_chatlog(
    data: ChatMessageRequest,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> bool:
    if not data.parts:
        data.parts = [
            ChatMessagePartRequest(
                type='text',
                text=data.message,
            )
        ]
    data_ = data.model_dump()
    if 'access_level' in data_:
        data_.pop('access_level')  # do we wanna save this?

    data_['parts'] = [part.model_dump(exclude_unset=True) for part in data.parts]

    async with get_session(session) as session:
        try:
            await session.execute(
                sa.insert(MChatlog.__table__).values(  # type: ignore
                    **data_,
                )
            )
        except sa.exc.IntegrityError as e:
            if 'uq_chatlogs_msg_id' in str(e):
                logger.info(
                    'Duplicate message id, ignoring', extra={'msg_id': data.msg_id}
                )
                return False
            raise e

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
        await database.redis.publish(  # type: ignore
            f'tbot:live_chat:{data.channel_id}',
            ChatMessage.model_validate(data).model_dump_json(),
        )
    return True
