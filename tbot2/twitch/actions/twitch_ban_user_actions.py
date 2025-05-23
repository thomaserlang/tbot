from uuid import UUID

from tbot2.channel_provider import get_channel_bot_provider
from tbot2.common.constants import (
    APP_TITLE,
    TBOT_CHANNEL_ID_HEADER,
)

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_bot_client


async def twitch_ban_user(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
    duration: int | None = None,
    reason: str | None = None,
) -> bool:
    bot_provider = await get_channel_bot_provider(
        provider='twitch',
        channel_id=channel_id,
    )
    if not bot_provider:
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
    data['data']['reason'] = f'{(reason or "")} [{APP_TITLE}]'

    response = await twitch_bot_client.post(
        url='/moderation/bans',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': bot_provider.provider_channel_id or '',
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


async def twitch_unban_user(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
) -> bool:
    bot_provider = await get_channel_bot_provider(
        provider='twitch',
        channel_id=channel_id,
    )
    if not bot_provider:
        raise ValueError(
            f'Failed to unban user {twitch_user_id} in channel '
            f'{channel_id}: no bot provider found'
        )
    response = await twitch_bot_client.delete(
        url='/moderation/bans',
        params={
            'broadcaster_id': broadcaster_id,
            'moderator_id': bot_provider.provider_channel_id or '',
            'user_id': twitch_user_id,
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
