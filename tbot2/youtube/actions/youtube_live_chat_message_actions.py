from tbot2.channel import ChannelOAuthProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER, TBOT_CHANNEL_PROVIDER_ID_HEADER
from tbot2.exceptions import InternalHttpError

from ..http_client import youtube_user_client
from ..schemas.youtube_live_chat_message_schema import LiveChatMessages


async def get_live_chat_messages(
    channel_provider: ChannelOAuthProvider,
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
            TBOT_CHANNEL_PROVIDER_ID_HEADER: str(channel_provider.id),
            'Authorization': f'Bearer {channel_provider.access_token}'
            if channel_provider.access_token
            else '',
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(response.status_code, response.text)
    
    return LiveChatMessages.model_validate(response.json())