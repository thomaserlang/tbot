from uuid import UUID

from tbot2.channel import get_channel_oauth_provider
from tbot2.common import TProvider
from tbot2.constants import APP_TITLE, TBOT_CHANNEL_ID_HEADER

from ..twitch_http_client import twitch_user_client


async def twitch_ban_user(
    channel_id: UUID,
    twitch_user_id: str,
    duration: int | None = None,
    reason: str | None = None,
):
    provider = await get_channel_oauth_provider(
        channel_id=channel_id,
        provider=TProvider.twitch,
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
    if duration:
        data['data']['duration'] = duration
    data['data']['reason'] = (reason or '') + f' [{APP_TITLE}]'

    response = await twitch_user_client.post(
        url='/moderation/bans',
        params={
            'broadcaster_id': provider.provider_user_id or '',
            'moderator_id': provider.provider_user_id or '',
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
        json=data,
    )
    response.raise_for_status()
    return True
