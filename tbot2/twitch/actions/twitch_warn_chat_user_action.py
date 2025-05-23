from uuid import UUID

from tbot2.channel_provider import get_channel_bot_provider
from tbot2.common.constants import APP_TITLE, TBOT_CHANNEL_ID_HEADER

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_bot_client


async def twitch_warn_chat_user(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
    reason: str | None = None,
) -> bool:
    provider = await get_channel_bot_provider(
        provider='twitch',
        channel_id=channel_id,
    )
    if not provider:
        raise ValueError(
            f'Failed to ban user {twitch_user_id} in channel '
            f'{channel_id}: no provider found'
        )

    data: dict[str, dict[str, str | int]] = {
        'data': {
            'user_id': twitch_user_id,
        }
    }
    data['data']['reason'] = f'{(reason or "")} [{APP_TITLE}]'

    response = await twitch_bot_client.post(
        url='/moderation/warnings',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': provider.provider_channel_id or '',
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
        json=data,
    )
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    return True
