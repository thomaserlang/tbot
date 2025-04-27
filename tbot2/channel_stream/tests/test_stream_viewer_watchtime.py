
from tbot2.testbase import run_file

"""
TODO: Issue with pytest loading the sqlalchemy models twice
resulting in weird errors when using orm.relationship

@pytest.mark.asyncio
async def test_stream_viewer_watchtime(db: None) -> None:
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )
    stream = await create_channel_provider_stream(
        channel_id=channel.id,
        provider='twitch',
        provider_id='123456789',
        provider_stream_id='123456789',
        started_at=datetime_now(),
    )

    await inc_stream_viewer_watchtime(
        channel_provider_stream_id=stream.id,
        provider_viewers=[
            ViewerNameHistoryRequest(
                provider_viewer_id='viewer1',
                name='viewer1',
                display_name='viewer1',
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
            ViewerNameHistoryRequest(
                provider_viewer_id='viewer2',
                name='viewer2',
                display_name='viewer2',
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
            ViewerNameHistoryRequest(
                provider_viewer_id='viewer1',
                name='viewer1',
                display_name='viewer1',
            ),
            ViewerNameHistoryRequest(
                provider_viewer_id='viewer2',
                name='viewer2',
                display_name='viewer2',
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
    assert viewer1_stats.last_channel_provider_stream
    assert viewer1_stats.last_channel_provider_stream.id == stream.id

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
    assert viewer1_stats.last_channel_provider_stream
    assert viewer1_stats.last_channel_provider_stream.id == stream.id
"""

if __name__ == '__main__':
    run_file(__file__)
