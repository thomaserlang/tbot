from uuid import UUID

import sqlalchemy as sa
from loguru import logger

from tbot2.channel_viewer import ViewerNameHistoryRequest, save_viewers_name_history
from tbot2.common import ChatMessage, ChatMessageRequest, Provider
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import database

from ..models.chatlog_model import MChatlog


async def get_chatlog(
    msg_id: str,
    channel_id: UUID | None = None,
    provider: Provider | None = None,
) -> ChatMessage | None:
    async with database.session() as session:
        stmt = (
            sa.select(MChatlog)
            .where(
                MChatlog.msg_id == msg_id,
            )
            .order_by(MChatlog.created_at.desc())
        )
        if channel_id:
            stmt = stmt.where(MChatlog.channel_id == channel_id)
        if provider:
            stmt = stmt.where(MChatlog.provider == provider)
        result = await session.scalar(stmt)
        return ChatMessage.model_validate(result) if result else None


async def create_chatlog(
    data: ChatMessageRequest,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> bool:
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
        await publish_chatlog(
            channel_id=data.channel_id,
            data=ChatMessage.model_validate(data),
        )
    return True


def chatlog_queue_key(channel_id: UUID) -> str:
    return f'tbot:channel-chatlog:{channel_id}'


async def publish_chatlog(
    channel_id: UUID,
    data: ChatMessage,
) -> None:
    key = chatlog_queue_key(channel_id=channel_id)
    await database.redis.publish(  # type: ignore
        key,
        data.model_dump_json(),
    )
