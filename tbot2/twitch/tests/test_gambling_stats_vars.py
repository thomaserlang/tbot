from datetime import datetime, timezone

import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_command import TCommand, fill_message
from tbot2.channel_gambling import (
    ChatterGamblingStatsUpdate,
    inc_chatter_gambling_stats,
)
from tbot2.common import ChatMessage, TProvider
from tbot2.testbase import run_file
from tbot2.twitch import cmd_var_fillers as cmd_var_fillers


@pytest.mark.asyncio
async def test_gambling_stats_vars(db: None):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    await inc_chatter_gambling_stats(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter',
        data=ChatterGamblingStatsUpdate(slots_wins=1, slots_losses=1),
    )

    message = await fill_message(
        response_message=(
            'Slots: {gambling_stats.slots_wins} wins, {gambling_stats.slots_loses} loses, '
            '{gambling_stats.slots_total_games} total games, {gambling_stats.slots_win_percent} win percent'
        ),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!gambling_stats',
            msg_id='123',
        ),
        command=TCommand(args=[], name='gambling_stats'),
    )

    assert message == 'Slots: 1 wins, 1 loses, 2 total games, 50.0% win percent'

    message = await fill_message(
        response_message=(
            'Roulette: {gambling_stats.roulette_wins} wins, {gambling_stats.roulette_loses} loses, '
            '{gambling_stats.roulette_total_games} total games, {gambling_stats.roulette_win_percent} win percent'
        ),
        chat_message=ChatMessage(
            type='message',
            created_at=datetime.now(tz=timezone.utc),
            provider=TProvider.twitch,
            provider_id='1234',
            channel_id=channel.id,
            chatter_id='test_chatter',
            chatter_name='test',
            chatter_display_name='Test',
            message='!gambling_stats',
            msg_id='123',
        ),
        command=TCommand(args=[], name='gambling_stats'),
    )

    assert message == 'Roulette: 0 wins, 0 loses, 0 total games, 0% win percent'


if __name__ == '__main__':
    run_file(__file__)
