from typing import Literal

from loguru import logger

from tbot2.channel import ChannelProvider
from tbot2.common import datetime_now
from tbot2.constants import TBOT_CHANNEL_ID_HEADER
from tbot2.exceptions import ErrorMessage, InternalHttpError

from ..exceptions import YouTubeError, YouTubeException
from ..http_client import youtube_user_client
from ..schemas.youtube_live_broadcast_schema import (
    LiveBroadcast,
    LiveBroadcastInsert,
    LiveBroadcastUpdate,
)
from ..schemas.youtube_page_schema import YoutubePage
from .youtube_live_stream_actions import (
    get_live_streams,
)

PART = {'id', 'snippet', 'status', 'content_details', 'monetizationDetails'}


async def get_live_broadcasts(
    channel_provider: ChannelProvider,
    broadcast_status: Literal['active', 'all', 'completed', 'upcoming'] | None = None,
    id: str | None = None,
    mine: bool | None = None,
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
        'part': ','.join(PART),
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
    params['maxResults'] = 2

    r = await youtube_user_client.get(
        '/liveBroadcasts',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params=params,
    )
    if r.status_code >= 400:
        if r.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(r.json()))
        raise InternalHttpError(r.status_code, r.text)
    page = YoutubePage[LiveBroadcast].model_validate(r.json())
    return page.items


async def create_live_broadcast(
    channel_provider: ChannelProvider,
    data: LiveBroadcastInsert,
) -> LiveBroadcast:
    r = await youtube_user_client.post(
        '/liveBroadcasts',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'part': ','.join(PART),
        },
        json=data.model_dump(exclude_unset=True, exclude_none=True, mode='json'),
    )
    if r.status_code >= 400:
        if r.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(r.json()))
        raise InternalHttpError(r.status_code, r.text)
    return LiveBroadcast.model_validate(r.json())


async def update_live_broadcast(
    channel_provider: ChannelProvider,
    snippet_title: str | None = None,
) -> LiveBroadcast:
    """
    TODO: Better way to patch the existing broadcast since values not
    specified gets reset to default
    """
    if not channel_provider.stream_id:
        raise ErrorMessage('No stream id found in channel provider')
    broadcasts = await get_live_broadcasts(
        channel_provider=channel_provider, id=channel_provider.stream_id
    )
    if not broadcasts:
        raise ErrorMessage(f'{channel_provider.stream_id} not found in live broadcasts')
    request = LiveBroadcastUpdate.model_validate(broadcasts[0])

    if snippet_title:
        request.snippet.title = snippet_title

    r = await youtube_user_client.put(
        '/liveBroadcasts',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'part': ','.join(PART),
        },
        json={
            'id': channel_provider.stream_id,
            **request.model_dump(exclude_unset=True, exclude_none=True, mode='json'),
        },
    )
    if r.status_code >= 400:
        if r.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(r.json()))
        raise InternalHttpError(r.status_code, r.text)
    return LiveBroadcast.model_validate(r.json())


async def bind_live_broadcast(
    channel_provider: ChannelProvider,
    live_broadcast_id: str,
    stream_id: str,
) -> LiveBroadcast:
    r = await youtube_user_client.post(
        '/liveBroadcasts/bind',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'part': ','.join(PART),
            'id': live_broadcast_id,
            'streamId': stream_id,
        },
    )
    if r.status_code >= 400:
        if r.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(r.json()))
        raise InternalHttpError(r.status_code, r.text)
    return LiveBroadcast.model_validate(r.json())


async def transition_live_broadcast(
    channel_provider: ChannelProvider,
    live_broadcast_id: str,
    status: Literal['live', 'complete'] = 'live',
) -> LiveBroadcast:
    r = await youtube_user_client.post(
        '/liveBroadcasts/transition',
        headers={
            TBOT_CHANNEL_ID_HEADER: str(channel_provider.channel_id),
        },
        params={
            'part': ','.join(PART),
            'id': live_broadcast_id,
            'broadcastStatus': status,
        },
    )
    if r.status_code >= 400:
        if r.headers.get('content-type').lower() == 'application/json':
            raise YouTubeException(YouTubeError.model_validate(r.json()))
        raise InternalHttpError(r.status_code, r.text)
    return LiveBroadcast.model_validate(r.json())


async def create_new_broadcast_from_previous(
    channel_provider: ChannelProvider,
    live_broadcast: LiveBroadcast | None = None,
    bind_to_prev_stream: bool = True,
) -> LiveBroadcast:
    if not live_broadcast:
        live_broadcasts = await get_live_broadcasts(
            channel_provider=channel_provider,
            broadcast_status='completed',
        )
        if not live_broadcasts:
            raise ValueError('No active broadcasts found')
        live_broadcast = live_broadcasts[0]
    broadcast_insert = LiveBroadcastInsert.model_validate(live_broadcast)
    broadcast_insert.snippet.scheduled_start_time = datetime_now()
    broadcast_insert.snippet.scheduled_end_time = None
    if broadcast_insert.content_details:
        broadcast_insert.content_details.enable_auto_start = True
        broadcast_insert.content_details.enable_auto_stop = True

    new_broadcast = await create_live_broadcast(
        channel_provider=channel_provider,
        data=broadcast_insert,
    )
    logger.debug(f'Created new broadcast {new_broadcast.id}')

    if not live_broadcast.content_details:
        raise ValueError('No content details in live broadcast')

    if bind_to_prev_stream:
        live_streams = await get_live_streams(
            channel_provider=channel_provider,
            id=live_broadcast.content_details.bound_stream_id,
            mine=True if not live_broadcast.content_details.bound_stream_id else None,
        )
        if live_streams:
            await bind_live_broadcast(
                channel_provider=channel_provider,
                live_broadcast_id=new_broadcast.id,
                stream_id=live_streams[0].id,
            )

    return new_broadcast
