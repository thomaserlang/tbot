from uuid import UUID

from tbot2.channel_provider import get_channel_bot_provider
from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.twitch.exceptions import TwitchException

from ..twitch_http_client import twitch_bot_client


async def twitch_delete_message(
    channel_id: UUID,
    broadcaster_id: str,
    message_id: str,
) -> bool:
    bot_provider = await get_channel_bot_provider(
        provider='twitch',
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
            'moderator_id': bot_provider.provider_channel_id or '',
            'message_id': message_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    return True
