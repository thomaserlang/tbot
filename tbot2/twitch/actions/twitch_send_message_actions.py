from uuid import UUID

from loguru import logger

from tbot2.bot_providers import BotProvider
from tbot2.channel import (
    SendChannelMessage,
    get_channel_bot_provider,
    get_channel_oauth_provider,
    on_send_channel_message,
)

from ..twitch_http_client import twitch_app_client


async def twitch_bot_send_message(
    channel_id: UUID,
    broadcaster_id: str,
    message: str,
    reply_parent_message_id: str | None = None,
    bot_provider: BotProvider | None = None,
) -> bool:
    if not bot_provider:
        bot_provider = await get_channel_bot_provider(
            provider='twitch',
            channel_id=channel_id,
        )
        if not bot_provider:
            raise ValueError(
                f'Failed to send message in channel {channel_id}: no bot provider found'
            )

    data = {
        'broadcaster_id': broadcaster_id,
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


@on_send_channel_message()
async def channel_send_message(data: SendChannelMessage) -> None:
    if data.provider != 'twitch' and data.provider != 'all':
        return

    channel_provider = await get_channel_oauth_provider(
        channel_id=data.channel_id,
        provider='twitch',
    )
    if not channel_provider:
        return

    bot_provider = channel_provider.bot_provider
    if not bot_provider:
        bot_provider = await get_channel_bot_provider(
            provider='twitch',
            channel_id=data.channel_id,
        )
        if not bot_provider:
            return

    await twitch_bot_send_message(
        channel_id=data.channel_id,
        broadcaster_id=channel_provider.provider_user_id or '',
        message=data.message,
        bot_provider=bot_provider,
    )
