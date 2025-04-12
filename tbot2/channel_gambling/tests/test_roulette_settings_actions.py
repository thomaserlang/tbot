import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_gambling import (
    RouletteSettingsUpdate,
    get_roulette_settings,
    update_roulette_settings,
)
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_roulette_settings(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    settings = await get_roulette_settings(channel_id=channel.id)
    assert settings.channel_id == channel.id
    assert settings.win_chance == 45

    settings = await update_roulette_settings(
        channel_id=channel.id,
        data=RouletteSettingsUpdate(win_chance=50),
    )
    assert settings.win_chance == 50


if __name__ == '__main__':
    run_file(__file__)
