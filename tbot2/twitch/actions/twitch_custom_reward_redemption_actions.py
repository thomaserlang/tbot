from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.twitch.exceptions import TwitchException

from ..schemas.event_channel_points_custom_reward_redemption_schema import (
    EventChannelPointsCustomRewardRedemption,
)
from ..twitch_http_client import twitch_user_client


async def get_custom_reward_redemption(
    *,
    broadcaster_id: str,
    id: str,
    channel_id: UUID,
) -> EventChannelPointsCustomRewardRedemption | None:
    response = await twitch_user_client.post(
        '/channel_points/custom_rewards/redemptions',
        params={
            'broadcaster_id': broadcaster_id,
            'id': id,
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
    data = response.json()
    if not data['data']:
        return None
    return EventChannelPointsCustomRewardRedemption.model_validate(data['data'][0])
