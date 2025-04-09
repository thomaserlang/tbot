from uuid import UUID

from tbot2.channel import get_channel_oauth_provider
from tbot2.common import TProvider

from ..twitch_http_client import twitch_app_client


async def twitch_send_message(
    channel_id: UUID,
    message: str,
    reply_parent_message_id: str | None = None,
):
    provider = await get_channel_oauth_provider(
        channel_id=channel_id,
        provider=TProvider.twitch,
    )
    if not provider:
        raise ValueError(
            f'Failed to send message in channel {channel_id}: no provider found'
        )
    data = {
        'broadcaster_id': provider.provider_user_id or '',
        'sender_id': provider.provider_user_id or '',
        'message': message,
    }
    if reply_parent_message_id:
        data['reply_parent_message_id'] = reply_parent_message_id

    response = await twitch_app_client.post(
        url='/chat/messages',
        json=data,
    )
    response.raise_for_status()
    return True
