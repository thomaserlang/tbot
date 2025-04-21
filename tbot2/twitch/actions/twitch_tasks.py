import asyncio
from datetime import datetime

from loguru import logger

from tbot2.channel_points import get_channel_point_settings, inc_bulk_points
from tbot2.channel_stream import (
    ChannelProviderStream,
    get_live_channels_provider_streams,
)
from tbot2.channel_viewer import ViewerNameHistoryRequest, inc_stream_viewer_watchtime
from tbot2.common import datetime_now

from .twitch_chatters_action import get_twitch_chatters

CHECK_EVERY = 60.0


async def task_update_live_streams() -> None:
    last_check: datetime | None = None
    logger.info('Starting Twitch task_update_live_streams')
    while True:
        if last_check:
            elapsed = (datetime_now() - last_check).total_seconds()
            sleep_time = max(0.0, CHECK_EVERY - elapsed)
        else:
            sleep_time = CHECK_EVERY
        await asyncio.sleep(sleep_time)
        last_check = datetime_now()

        streams = await get_live_channels_provider_streams(provider='twitch')
        await asyncio.gather(
            *[update_viewers_stream_data(stream) for stream in streams],
        )


async def update_viewers_stream_data(stream: ChannelProviderStream) -> None:
    try:
        logger.debug(
            'Updating viewer stream data for '
            f'{stream.channel_id} {stream.provider_stream_id}'
        )
        point_settings = await get_channel_point_settings(channel_id=stream.channel_id)
        async for chatters in await get_twitch_chatters(
            channel_id=stream.channel_id,
            broadcaster_id=stream.provider_id,
        ):
            if point_settings.enabled:
                await inc_bulk_points(
                    channel_id=stream.channel_id,
                    provider='twitch',
                    provider_viewer_ids=[chatter.user_id for chatter in chatters],
                    points=point_settings.points_per_min,
                )
            await inc_stream_viewer_watchtime(
                channel_provider_stream_id=stream.id,
                provider_viewers=[
                    ViewerNameHistoryRequest(
                        provider_viewer_id=chatter.user_id,
                        name=chatter.user_login,
                        display_name=chatter.user_name,
                    )
                    for chatter in chatters
                ],
                watchtime=int(CHECK_EVERY),
            )
    except Exception as e:
        logger.exception(e)
