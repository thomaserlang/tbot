from loguru import logger
from uuid6 import uuid7

from tbot2.channel import ChannelOAuthProvider
from tbot2.channel_chatlog import create_chatlog
from tbot2.common import ChatMessage
from tbot2.database import database

from ..schemas.youtube_live_chat_message_schema import LiveChatMessage


async def handle_message(
    channel_provider: ChannelOAuthProvider,
    message: LiveChatMessage,
) -> None:
    logger.debug(f'Handling message: {message.snippet.display_message}')
    match message.snippet.type:
        case 'superChatEvent':
            logger.debug(
                f'New super chat message: {message.snippet.display_message}'
            )
        case 'textMessageEvent':
            await handle_text_message_event(
                channel_provider=channel_provider, message=message
            )
        case _:
            logger.debug(f'Unknown message type: {message.snippet.type}')


async def handle_text_message_event(
    channel_provider: ChannelOAuthProvider,
    message: LiveChatMessage,
) -> None:
    
    chat_message = ChatMessage(
        id=uuid7(),
        type='message',
        channel_id=channel_provider.channel_id,
        provider_viewer_id=message.author_details.channel_id,
        viewer_name=message.author_details.display_name,
        viewer_display_name=message.author_details.display_name,
        viewer_color='',
        created_at=message.snippet.published_at,
        message=message.snippet.display_message,
        msg_id=message.id,
        provider='youtube',
        provider_id=channel_provider.provider_user_id or '',
    )
    await create_chatlog(data=chat_message)
    await database.redis.publish(  # type: ignore
        f'tbot:live_chat:{chat_message.channel_id}', chat_message.model_dump_json()
    )