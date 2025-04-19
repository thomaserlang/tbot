
from loguru import logger

from tbot2.channel import (
    ChannelProvider,
    SendChannelMessage,
    on_send_channel_provider_message,
)

from ..twitch_http_client import twitch_app_client


async def twitch_bot_send_message(
    channel_provider: ChannelProvider,
    message: str,
    reply_parent_message_id: str | None = None,
) -> bool:
    bot_provider = await channel_provider.get_default_or_system_bot_provider()
    data = {
        'broadcaster_id': channel_provider.provider_user_id or '',
        'sender_id': bot_provider.provider_user_id or '',
        'message': message,
    }
    if reply_parent_message_id:
        data['reply_parent_message_id'] = reply_parent_message_id

    response = await twitch_app_client.post(
        url='/chat/messages',
        json=data,
    )
    if response.status_code >= 400:
        logger.error(f'twitch_bot_send_message: {response.status_code} {response.text}')
        return False
    return True


@on_send_channel_provider_message('twitch')
async def send_channel_message(data: SendChannelMessage) -> None:
    await twitch_bot_send_message(
        channel_provider=data.channel_provider,
        message=data.message,
    )
