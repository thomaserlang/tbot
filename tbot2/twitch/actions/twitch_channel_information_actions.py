from uuid import UUID

from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import InternalHttpError

from ..schemas.twitch_channel_information_schema import (
    ChannelInformation,
    ModifyChannelInformationRequest,
)
from ..twitch_http_client import twitch_user_client


async def update_twitch_channel_information(
    channel_id: UUID, broadcaster_id: str, data: ModifyChannelInformationRequest
) -> bool:
    response = await twitch_user_client.patch(
        url='/channels',
        json=data.model_dump(exclude_unset=True, mode='json'),
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
        params={
            'broadcaster_id': broadcaster_id,
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(
            status_code=response.status_code,
            body=f'{response.text}',
        )
    return True


async def get_twitch_channel_information(
    channel_id: UUID, broadcaster_id: str
) -> ChannelInformation | None:
    response = await twitch_user_client.get(
        url='/channels',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_id),
        },
        params={
            'broadcaster_id': broadcaster_id,
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(
            status_code=response.status_code,
            body=f'{response.text}',
        )
    data = response.json()
    if not data['data']:
        return None
    return ChannelInformation.model_validate(data['data'][0])
