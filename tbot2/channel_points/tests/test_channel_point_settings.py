import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_points.actions.channel_point_settings_actions import (
    get_channel_point_settings,
    update_channel_point_settings,
)
from tbot2.channel_points.schemas.channel_point_settings_schema import (
    ChannelPointSettingsUpdate,
)
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_channel_point_settings(db: None):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    settings = await get_channel_point_settings(channel_id=channel.id)
    assert settings.channel_id == channel.id
    assert settings.points_name == 'points'
    assert settings.enabled is False

    settings = await update_channel_point_settings(
        channel_id=channel.id,
        data=ChannelPointSettingsUpdate(points_name='test_points', enabled=True),
    )
    assert settings.channel_id == channel.id
    assert settings.points_name == 'test_points'
    assert settings.enabled is True

    settings = await get_channel_point_settings(channel_id=channel.id)
    assert settings.points_name == 'test_points'
    assert settings.enabled is True


if __name__ == '__main__':
    run_file(__file__)
