from uuid import UUID

from loguru import logger

from tbot2.common.constants import TBOT_CHANNEL_ID_HEADER

from ..exceptions import TwitchException
from ..schemas.twitch_commercial_schema import RunCommercialResponse
from ..twitch_http_client import twitch_user_client


async def twitch_run_commercial(
    channel_id: UUID,
    broadcaster_id: str,
    length: int = 180,
) -> RunCommercialResponse:
    response = await twitch_user_client.post(
        '/channels/commercial',
        json={
            'broadcaster_id': broadcaster_id,
            'length': length,
        },
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
    )
    if response.status_code >= 400:
        if response.status_code == 429:
            data = response.json()
            logger.info(data)
            raise TwitchException(
                response=response,
                request=response.request,
                message='Too early to run another commercial',
            )
        raise TwitchException(
            response=response,
            request=response.request,
        )
    data = response.json()
    return RunCommercialResponse.model_validate(data['data'][0])
