from uuid import UUID

from tbot2.channel import get_channel_oauth_provider
from tbot2.common import TProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER

from ..twitch_http_client import twitch_user_client


async def twitch_delete_message(
    channel_id: UUID,
    message_id: str,
):
    provider = await get_channel_oauth_provider(
        channel_id=channel_id,
        provider=TProvider.twitch,
    )
    if not provider:
        raise ValueError(
            f'Failed to delete message {message_id} in channel '
            f'{channel_id}: no provider found'
        )
    response = await twitch_user_client.delete(
        url='/moderation/chat',
        params={
            'broadcaster_id': provider.provider_user_id or '',
            'moderator_id': provider.provider_user_id or '',
            'message_id': message_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    response.raise_for_status()
    return True
