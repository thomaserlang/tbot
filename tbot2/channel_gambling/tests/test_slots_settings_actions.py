import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_gambling import (
    SlotsSettingsUpdate,
    get_slots_settings,
    update_slots_settings,
)
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_slots_settings(db: None):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    settings = await get_slots_settings(channel_id=channel.id)
    assert settings.channel_id == channel.id
    assert settings.payout_percent == 95

    settings = await update_slots_settings(
        channel_id=channel.id,
        data=SlotsSettingsUpdate(payout_percent=90),
    )
    assert settings.payout_percent == 90

if __name__ == '__main__':
    run_file(__file__)