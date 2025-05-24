from uuid import UUID

from loguru import logger

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import TwitchException
from ..twitch_http_client import twitch_user_client


async def twitch_add_channel_moderator(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
) -> bool:
    response = await twitch_user_client.post(
        url='/moderation/moderators',
        params={
            'broadcaster_id': broadcaster_id,
            'user_id': twitch_user_id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        if 'user is already a mod' in response.text:
            logger.info(
                f'User {twitch_user_id} is already a moderator for '
                f'channel {broadcaster_id}.',
            )
            return False
        raise TwitchException(
            response=response,
            request=response.request,
        )
    return True


async def twitch_remove_channel_moderator(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
) -> bool:
    response = await twitch_user_client.post(
        url='/moderation/moderators',
        params={
            'broadcaster_id': broadcaster_id,
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
