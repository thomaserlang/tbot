import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_viewer_stats import (
    get_channel_viewer_stats,
    get_stream_viewer_watchtime,
    inc_stream_viewer_watchtime,
)
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_stream_viewer_watchtime(db: None):
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )

    await inc_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_ids={'viewer1'},
        watchtime=100,
    )

    viewer1 = await get_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_id='viewer1',
    )
    assert viewer1 is not None
    assert viewer1.watchtime == 100

    await inc_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_ids={'viewer2'},
        watchtime=100,
    )

    viewer2 = await get_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_id='viewer2',
    )
    assert viewer2 is not None
    assert viewer2.watchtime == 100

    await inc_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_ids={'viewer1', 'viewer2'},
        watchtime=100,
    )
    viewer1 = await get_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_id='viewer1',
    )
    assert viewer1 is not None
    assert viewer1.watchtime == 200
    viewer2 = await get_stream_viewer_watchtime(
        channel_id=channel.id,
        provider='twitch',
        stream_id='123456789',
        viewer_id='viewer2',
    )
    assert viewer2 is not None
    assert viewer2.watchtime == 200

    viewer1_stats = await get_channel_viewer_stats(
        channel_id=channel.id,
        provider='twitch',
        viewer_id='viewer1',
    )
    assert viewer1_stats is not None
    assert viewer1_stats.streams == 1
    assert viewer1_stats.streams_row == 1
    assert viewer1_stats.streams_row_peak == 1
    assert viewer1_stats.streams_row_peak_date is not None
    assert viewer1_stats.last_stream_id == '123456789'

    viewer2_stats = await get_channel_viewer_stats(
        channel_id=channel.id,
        provider='twitch',
        viewer_id='viewer2',
    )
    assert viewer2_stats is not None
    assert viewer2_stats.streams == 1
    assert viewer2_stats.streams_row == 1
    assert viewer2_stats.streams_row_peak == 1
    assert viewer2_stats.streams_row_peak_date is not None
    assert viewer2_stats.last_stream_id == '123456789'
    assert viewer2_stats.last_stream_at is not None


if __name__ == '__main__':
    run_file(__file__)
