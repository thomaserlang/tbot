from uuid import UUID

from tbot2.channel import get_channel_bot_provider
from tbot2.common import TProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER

from ..twitch_http_client import twitch_bot_client


async def twitch_delete_message(
    channel_id: UUID,
    broadcaster_id: str,
    message_id: str,
):
    bot_provider = await get_channel_bot_provider(
        provider=TProvider.twitch,
        channel_id=channel_id,
    )
    if not bot_provider:
        raise ValueError(
            f'Failed to delete message {message_id} in channel '
            f'{channel_id}: no provider found'
        )
    response = await twitch_bot_client.delete(
        url='/moderation/chat',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': bot_provider.provider_user_id or '',
            'message_id': message_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
            'Authorization': f'Bearer {bot_provider.access_token}',
        },
    )
    response.raise_for_status()
    return True
