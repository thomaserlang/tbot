import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_points.actions.chatter_point_actions import (
    get_points,
    inc_bulk_points,
    inc_points,
)
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_point_actions(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
        points=10,
    )

    points = await get_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
    )
    assert points.points == 10

    points = await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
        points=10,
    )
    assert points.points == 20

    points = await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
        points=-5,
    )
    assert points.points == 15

    points = await get_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
    )
    assert points.points == 15

    points = await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='123',
        points=-1000,
    )
    assert points.points == 0


@pytest.mark.asyncio
async def test_inc_bulk_points(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    await inc_bulk_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_ids=['1', '2'],
        points=10,
    )

    points = await get_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='1',
    )
    assert points.points == 10

    points = await get_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='2',
    )
    assert points.points == 10


if __name__ == '__main__':
    run_file(__file__)
