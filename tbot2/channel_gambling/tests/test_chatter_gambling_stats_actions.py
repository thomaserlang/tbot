import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_gambling import (
    ChatterGamblingStatsUpdate,
    get_chatter_gambling_stats,
    inc_chatter_gambling_stats,
)
from tbot2.common import TProvider
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_chatter_gambling_stats(db: None):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    stats = await get_chatter_gambling_stats(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter',
    )
    assert stats.channel_id == channel.id
    assert stats.chatter_id == 'test_chatter'
    assert stats.provider == TProvider.twitch
    assert stats.slots_wins == 0
    assert stats.slots_losses == 0
    assert stats.roulette_wins == 0
    assert stats.roulette_losses == 0

    stats = await inc_chatter_gambling_stats(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter',
        data=ChatterGamblingStatsUpdate(slots_wins=1, slots_losses=1),
    )

    assert stats.slots_wins == 1
    assert stats.slots_losses == 1
    assert stats.roulette_wins == 0
    assert stats.roulette_losses == 0


if __name__ == '__main__':
    run_file(__file__)
