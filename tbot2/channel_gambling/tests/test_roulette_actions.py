from unittest.mock import patch

import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_gambling import roulette
from tbot2.channel_points import inc_points
from tbot2.common import TProvider
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_roulette_actions(db: None):
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    with pytest.raises(ValueError, match='Not enough points to bet'):
        await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet=100,
        )

    await inc_points(
        channel_id=channel.id,
        provider=TProvider.twitch,
        chatter_id='test_chatter',
        points=100,
    )

    with pytest.raises(ValueError, match='Bet is too low, minimum is 5'):
        await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet=4,
        )

    with pytest.raises(ValueError, match='Invalid points: invalid'):
        await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet='invalid',
        )

    with pytest.raises(ValueError, match='Not enough points to bet'):
        await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet='101%',
        )

    def mock_win_random_int():
        return 0

    with patch(
        'tbot2.channel_gambling.actions.roulette_actions.random_int',
        mock_win_random_int,
    ):
        result = await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet=50,
        )
        assert result.won
        assert result.message == '@{user}, You won 50 points and now have 150 points'

    def mock_lose_random_int():
        return 100

    with patch(
        'tbot2.channel_gambling.actions.roulette_actions.random_int',
        mock_lose_random_int,
    ):
        result = await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet=50,
        )
        assert not result.won
        assert result.message == '@{user}, You lost 50 points and now have 100 points'

    with patch(
        'tbot2.channel_gambling.actions.roulette_actions.random_int',
        mock_win_random_int,
    ):
        result = await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet='50%',
        )
        assert result.won
        assert result.message == '@{user}, You won 50 points and now have 150 points'

    with patch(
        'tbot2.channel_gambling.actions.roulette_actions.random_int',
        mock_win_random_int,
    ):
        result = await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet='all',
        )
        assert result.won
        assert result.message == '@{user}, You won 150 points and now have 300 points'

    with patch(
        'tbot2.channel_gambling.actions.roulette_actions.random_int',
        mock_lose_random_int,
    ):
        result = await roulette(
            channel_id=channel.id,
            provider=TProvider.twitch,
            chatter_id='test_chatter',
            bet='all',
        )
        assert not result.won
        assert result.message == '@{user}, You lost 300 points and now have 0 points'


if __name__ == '__main__':
    run_file(__file__)
