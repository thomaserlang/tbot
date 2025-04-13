import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_stats import (
    create_channel_provider_stream,
    get_channel_viewer_stats,
    get_stream_viewer_watchtime,
    inc_stream_viewer_watchtime,
)
from tbot2.chatlog import ChatterRequest
from tbot2.common import TProvider, datetime_now
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_stream_viewer_watchtime(db: None) -> None:
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )
    stream = await create_channel_provider_stream(
        channel_id=channel.id,
        provider=TProvider.twitch,
        provider_id='123456789',
        provider_stream_id='123456789',
        started_at=datetime_now(),
    )

    await inc_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewers=[
            ChatterRequest(
                chatter_id='viewer1',
                chatter_name='viewer1',
                chatter_display_name='viewer1',
            )
        ],
        watchtime=100,
    )

    viewer1 = await get_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewer_id='viewer1',
    )
    assert viewer1 is not None
    assert viewer1.watchtime == 100

    await inc_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewers=[
            ChatterRequest(
                chatter_id='viewer2',
                chatter_name='viewer2',
                chatter_display_name='viewer2',
            )
        ],
        watchtime=100,
    )

    viewer2 = await get_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewer_id='viewer2',
    )
    assert viewer2 is not None
    assert viewer2.watchtime == 100

    await inc_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewers=[
            ChatterRequest(
                chatter_id='viewer1',
                chatter_name='viewer1',
                chatter_display_name='viewer1',
            ),
            ChatterRequest(
                chatter_id='viewer2',
                chatter_name='viewer2',
                chatter_display_name='viewer2',
            ),
        ],
        watchtime=100,
    )
    viewer1 = await get_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewer_id='viewer1',
    )
    assert viewer1 is not None
    assert viewer1.watchtime == 200
    viewer2 = await get_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewer_id='viewer2',
    )
    assert viewer2 is not None
    assert viewer2.watchtime == 200

    viewer1_stats = await get_channel_viewer_stats(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='viewer1',
    )
    assert viewer1_stats is not None
    assert viewer1_stats.streams == 1
    assert viewer1_stats.streams_row == 1
    assert viewer1_stats.streams_row_peak == 1
    assert viewer1_stats.streams_row_peak_date is not None
    assert viewer1_stats.last_channel_provider_stream_id == stream.id

    viewer2_stats = await get_channel_viewer_stats(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='viewer2',
    )
    assert viewer2_stats is not None
    assert viewer2_stats.streams == 1
    assert viewer2_stats.streams_row == 1
    assert viewer2_stats.streams_row_peak == 1
    assert viewer2_stats.streams_row_peak_date is not None
    assert viewer2_stats.last_channel_provider_stream_id == stream.id


if __name__ == '__main__':
    run_file(__file__)
