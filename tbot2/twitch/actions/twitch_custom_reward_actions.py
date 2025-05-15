from uuid import UUID

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import TwitchException
from ..schemas.twitch_custom_reward_schema import CustomReward, CustomRewardResponse
from ..twitch_http_client import twitch_user_client


async def get_custom_reward(
    *,
    channel_id: UUID,
    broadcaster_id: str,
    id: str,
) -> CustomReward | None:
    response = await twitch_user_client.post(
        '/channel_points/custom_rewards',
        params={
            'broadcaster_id': broadcaster_id,
            'id': id,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code == 404:
        return None
    if response.status_code >= 400:
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = CustomRewardResponse.model_validate(response.json())
    if not data.data:
        return None
    return data.data[0]
