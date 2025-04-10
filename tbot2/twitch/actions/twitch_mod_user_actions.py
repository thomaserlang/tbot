import logging
from uuid import UUID

from tbot2.constants import TBOT_CHANNEL_ID_HEADER

from ..twitch_http_client import twitch_user_client


async def twitch_add_channel_moderator(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
):
    try:
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
        response.raise_for_status()
        return True
    except Exception as e:
        logging.exception(e)
        return False


async def twitch_remove_channel_moderator(
    channel_id: UUID,
    broadcaster_id: str,
    twitch_user_id: str,
):
    try:
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
        response.raise_for_status()
        return True
    except Exception as e:
        logging.exception(e)
        return False
