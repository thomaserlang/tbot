from tbot2.channel_provider import ChannelProvider

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_app_client


async def twitch_bot_send_message(
    channel_provider: ChannelProvider,
    message: str,
    reply_parent_message_id: str | None = None,
) -> bool:
    bot_provider = await channel_provider.get_default_or_system_bot_provider()
    data = {
        'broadcaster_id': channel_provider.provider_channel_id or '',
        'sender_id': bot_provider.provider_channel_id or '',
        'message': message,
    }
    if reply_parent_message_id:
        data['reply_parent_message_id'] = reply_parent_message_id

    response = await twitch_app_client.post(
        url='/chat/messages',
        json=data,
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    return True
