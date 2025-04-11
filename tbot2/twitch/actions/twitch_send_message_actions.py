import logging
from uuid import UUID

from tbot2.bot_providers import BotProvider
from tbot2.channel import get_channel_bot_provider
from tbot2.common import TProvider

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
            provider=TProvider.twitch,
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
        logging.error(
            f'twitch_bot_send_message: {response.status_code} {response.text}'
        )
        return False
    return True
