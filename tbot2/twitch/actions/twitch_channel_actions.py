from tbot2.channel import ChannelProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import InternalHttpError

from ..schemas.twitch_channel_schema import ModifyChannelInformationRequest
from ..twitch_http_client import twitch_user_client


async def update_twitch_channel(
    channel_provider: ChannelProvider, data: ModifyChannelInformationRequest
) -> bool:
    response = await twitch_user_client.patch(
        url='/channels',
        json=data.model_dump(exclude_unset=True, mode='json'),
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'broadcaster_id': channel_provider.provider_user_id or '',
        },
    )
    if response.status_code >= 400:
        raise InternalHttpError(
            status_code=response.status_code,
            body=f'{response.text}',
        )
    return True
