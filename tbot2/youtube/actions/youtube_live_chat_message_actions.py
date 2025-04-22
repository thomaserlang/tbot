from loguru import logger

from tbot2.channel import (
    ChannelProvider,
)
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import InternalHttpError

from ..exceptions import YouTubeError, YouTubeException
from ..http_client import youtube_bot_client, youtube_user_client
from ..schemas.youtube_live_chat_message_schema import LiveChatMessages


async def get_live_chat_messages(
    channel_provider: ChannelProvider,
    live_chat_id: str,
    page_token: str,
) -> LiveChatMessages:
    params: dict[str, str] = {
        'liveChatId': live_chat_id,
        'pageToken': page_token,
        'part': 'snippet,authorDetails',
    }
    response = await youtube_user_client.get(
        '/liveChat/messages',
        params=params,
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
    )
    if response.status_code >= 400:
        if response.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(response.json()))
        raise InternalHttpError(response.status_code, response.text)

    return LiveChatMessages.model_validate(response.json())


async def send_live_chat_message(
    channel_provider: ChannelProvider,
    live_chat_id: str,
    message: str,
) -> bool:
    bot_provider = channel_provider.bot_provider
    if not bot_provider:
        bot_provider = await channel_provider.get_default_or_system_bot_provider()
    response = await youtube_bot_client.post(
        url='/liveChat/messages',
        params={
            'part': 'snippet',
        },
        json={
            'snippet': {
                'liveChatId': live_chat_id,
                'type': 'textMessageEvent',
                'textMessageDetails': {
                    'messageText': message,
                },
            },
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
    )
    if response.status_code >= 400:
        logger.error(f'send_live_chat_message: {response.status_code} {response.text}')
        return False
    return True


async def delete_live_chat_message(
    channel_provider: ChannelProvider,
    message_id: str,
) -> bool:
    response = await youtube_bot_client.delete(
        url='/liveChat/messages',
        params={
            'id': message_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
    )
    if response.status_code >= 400:
        logger.error(f'bot_delete_message: {response.status_code} {response.text}')
        return False
    return True
