import asyncio
from datetime import datetime

from loguru import logger

from tbot2.channel_points import get_channel_point_settings, inc_bulk_points
from tbot2.channel_provider import (
    ChannelProvider,
    ChannelProviderOAuthNotFound,
    get_channels_providers,
)
from tbot2.channel_stream import (
    add_viewer_count,
    end_channel_provider_stream,
)
from tbot2.channel_viewer import ViewerNameHistoryRequest, inc_stream_viewer_watchtime
from tbot2.common import datetime_now
from tbot2.common.utils.chunk_list import chunk_list

from .twitch_chatters_action import get_twitch_chatters
from .twitch_streams_action import get_twitch_streams

CHECK_EVERY = 60.0


async def twitch_tasks() -> None:
    last_check: datetime | None = None
    logger.info('Starting twitch_tasks')
    while True:
        if last_check:
            elapsed = (datetime_now() - last_check).total_seconds()
            sleep_time = max(0.0, CHECK_EVERY - elapsed)
        else:
            sleep_time = CHECK_EVERY
        await asyncio.sleep(sleep_time)
        last_check = datetime_now()

        channel_providers: list[ChannelProvider] = []
        async for channel_provider in get_channels_providers(
            provider='twitch', stream_live=True
        ):
            channel_providers.append(channel_provider)
        try:
            await asyncio.gather(
                update_viewer_count(channel_providers=channel_providers),
                *[
                    update_channel_providers_viewer_watchtime(channel_provider)
                    for channel_provider in channel_providers
                ],
            )
        except Exception as e:
            logger.exception(e)
            continue


@logger.catch()
async def update_viewer_count(channel_providers: list[ChannelProvider]) -> None:
    logger.debug('Updating viewer count')
    for chunk in chunk_list(channel_providers, 100):
        provider_channel_ids = [
            channel_provider.provider_channel_id
            for channel_provider in chunk
            if channel_provider.provider_channel_id
        ]
        streams = await get_twitch_streams(user_ids=provider_channel_ids)

        streams_by_user_id = {stream.user_id: stream for stream in streams}
        for channel_provider in chunk:
            stream = streams_by_user_id.get(channel_provider.provider_channel_id or '')
            if not stream or not channel_provider.channel_provider_stream_id:
                continue
            if channel_provider.stream_viewer_count == stream.viewer_count:
                continue
            await add_viewer_count(
                channel_provider_id=channel_provider.id,
                channel_provider_stream_id=channel_provider.channel_provider_stream_id,
                viewer_count=stream.viewer_count,
            )
    logger.debug('Finished updating viewer count')


@logger.catch()
async def update_channel_providers_viewer_watchtime(
    channel_provider: ChannelProvider,
) -> None:
    with logger.contextualize(channel_provider_id=channel_provider.id):
        try:
            await update_viewer_watchtime(channel_provider=channel_provider)
        except ChannelProviderOAuthNotFound:
            logger.info('Channel provider oauth no longer exists, ending stream')
            await end_channel_provider_stream(
                channel_id=channel_provider.channel_id,
                provider='twitch',
                ended_at=datetime_now(),
            )
        except Exception as e:
            logger.exception(e)


async def update_viewer_watchtime(channel_provider: ChannelProvider) -> None:
    logger.debug('Updating viewer watchtime')
    if (
        channel_provider.scope
        and 'moderator:read:chatters' not in channel_provider.scope
    ):
        logger.info('Channel provider does not have moderator:read:chatters scope')
        return

    point_settings = await get_channel_point_settings(
        channel_id=channel_provider.channel_id
    )
    async for chatters in await get_twitch_chatters(
        channel_id=channel_provider.channel_id,
        broadcaster_id=channel_provider.provider_channel_id or '',
    ):
        if point_settings.enabled:
            await inc_bulk_points(
                channel_id=channel_provider.channel_id,
                provider='twitch',
                provider_viewer_ids=[chatter.user_id for chatter in chatters],
                points=point_settings.points_per_min,
            )
        await inc_stream_viewer_watchtime(
            channel_provider_stream_id=channel_provider.channel_provider_stream_id,  # type: ignore
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
