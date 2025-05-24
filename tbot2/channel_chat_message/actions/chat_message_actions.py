from uuid import UUID

import sqlalchemy as sa
from loguru import logger

from tbot2.channel_viewer import ViewerNameHistoryRequest, save_viewers_name_history
from tbot2.common import (
    ChatMessage,
    ChatMessageCreate,
    ErrorMessage,
    Provider,
    PubSubEvent,
)
from tbot2.contexts import AsyncSession, get_session
from tbot2.database import conn

from ..models.chat_message_model import MChatMessage


async def get_chat_message(
    msg_id: str,
    channel_id: UUID | None = None,
    provider: Provider | None = None,
) -> ChatMessage | None:
    async with conn.session() as session:
        stmt = (
            sa.select(MChatMessage)
            .where(
                MChatMessage.provider_message_id == msg_id,
            )
            .order_by(MChatMessage.created_at.desc())
        )
        if channel_id:
            stmt = stmt.where(MChatMessage.channel_id == channel_id)
        if provider:
            stmt = stmt.where(MChatMessage.provider == provider)
        result = await session.scalar(stmt)
        return ChatMessage.model_validate(result) if result else None


async def create_chat_message(
    data: ChatMessageCreate,
    publish: bool = True,
    session: AsyncSession | None = None,
) -> ChatMessage:
    data_ = data.model_dump()
    if 'access_level' in data_:
        data_.pop('access_level')  # do we wanna save this?

    data_['message_parts'] = [
        part.model_dump(exclude_unset=True) for part in data.message_parts
    ]
    if data.notice_message_parts is not None:
        data_['notice_message_parts'] = [
            part.model_dump(exclude_unset=True) for part in data.notice_message_parts
        ]

    async with get_session(session) as session:
        try:
            await session.execute(
                sa.insert(MChatMessage.__table__).values(  # type: ignore
                    **data_,
                )
            )
        except sa.exc.IntegrityError as e:
            if 'uq_chatlogs_msg_id' in str(e):
                logger.debug(
                    'Duplicate message id, ignoring',
                    extra={'provider_message_id': data.provider_message_id},
                )
                raise ErrorMessage(
                    'Duplicate message id, ignoring',
                    type='duplicate_provider_message_id',
                    code=409,
                ) from e
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

    chat_message = ChatMessage.model_validate(data)
    if publish:
        await publish_chat_message(
            channel_id=data.channel_id,
            event=PubSubEvent[ChatMessage](
                type='chat_message', action='new', data=chat_message
            ),
        )
    return chat_message


def chat_message_queue_key(channel_id: UUID) -> str:
    return f'tbot:channel-chat-message:{channel_id}'


async def publish_chat_message(
    channel_id: UUID,
    event: PubSubEvent[ChatMessage],
) -> None:
    key = chat_message_queue_key(channel_id=channel_id)
    await conn.redis.publish(  # type: ignore
        key,
        event.model_dump_json(),
    )
