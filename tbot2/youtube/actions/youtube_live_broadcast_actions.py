from typing import Literal

from tbot2.channel import ChannelOAuthProvider
from tbot2.constants import TBOT_CHANNEL_ID_HEADER, TBOT_CHANNEL_PROVIDER_ID_HEADER
from tbot2.exceptions import InternalHttpError

from ..http_client import youtube_user_client
from ..schemas.youtube_live_broadcast_schema import LiveBroadcast
from ..schemas.youtube_page_schema import YoutubePage


async def get_live_broadcasts(
    channel_provider: ChannelOAuthProvider,
    broadcast_status: Literal['active', 'all', 'completed', 'upcoming'] | None = None,
    id: str | None = None,
    mine: bool | None = True,
    broadcast_type: Literal['all', 'event', 'persistent'] = 'all',
) -> list[LiveBroadcast]:
    """
    Get live broadcasts for a channel.

    Either `broadcast_status`, `id` or `mine` must be specified.

    Params:
        id:
            The id parameter specifies a comma-separated list of YouTube broadcast IDs
            that identify the broadcasts being retrieved. In a liveBroadcast resource,
            the id property specifies the broadcast's ID.

        mine:
            The mine parameter can be used to instruct the API to only return
            broadcasts owned by the authenticated user. Set the parameter value to
            true to only retrieve your own broadcasts.

        broadcast_type:
            The broadcastType parameter filters the API response to only include
            broadcasts with the specified type. The parameter should be used in
            requests that set the mine parameter to true or that use the
            broadcast_status parameter.
    """
    params: dict[str, str | bool | int] = {
        'part': ','.join(
            {'id', 'snippet', 'contentDetails', 'status', 'monetizationDetails'}
        ),
    }
    if not broadcast_status and not id and not mine:
        raise ValueError('Either broadcast_status, id or mine must be specified')

    if broadcast_status:
        params['broadcast_status'] = broadcast_status
    if id:
        params['id'] = id
    if mine:
        params['mine'] = mine
    if broadcast_type:
        params['broadcastType'] = broadcast_type
    params['maxResults'] = 50

    r = await youtube_user_client.get(
        '/liveBroadcasts',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
            TBOT_CHANNEL_PROVIDER_ID_HEADER: str(channel_provider.id),
        },
        params=params,
    )
    if r.status_code >= 400:
        raise InternalHttpError(r.status_code, r.text)
    page = YoutubePage[LiveBroadcast].model_validate(r.json())
    return page.items
