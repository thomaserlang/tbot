from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import YouTubeException
from ..http_client import youtube_bot_client, youtube_user_client
from ..schemas.youtube_live_chat_message_schema import LiveChatMessages


async def get_live_chat_messages(
    channel_id: UUID,
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
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)

    return LiveChatMessages.model_validate(response.json())


async def send_live_chat_message(
    channel_id: UUID,
    live_chat_id: str,
    message: str,
) -> bool:
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
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    return True


async def delete_live_chat_message(
    channel_id: UUID,
    message_id: str,
) -> bool:
    response = await youtube_bot_client.delete(
        url='/liveChat/messages',
        params={
            'id': message_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise YouTubeException(response=response, request=response.request)
    return True
