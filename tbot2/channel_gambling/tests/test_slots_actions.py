from unittest.mock import patch

import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.channel_gambling import slots
from tbot2.channel_points import inc_points
from tbot2.exceptions import ErrorMessage
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_roulette_actions(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))

    with pytest.raises(ErrorMessage, match='Not enough points to bet 100'):
        await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet=100,
        )

    await inc_points(
        channel_id=channel.id,
        provider='twitch',
        provider_viewer_id='test_chatter',
        points=100,
    )

    with pytest.raises(ErrorMessage, match='Bet is too low, minimum is 5'):
        await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet=4,
        )

    with pytest.raises(ErrorMessage, match='Invalid points: invalid'):
        await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet='invalid',
        )

    with pytest.raises(ErrorMessage, match='Not enough points to bet'):
        await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet='101%',
        )

    def mock_win_random_choices(emotes: list[str]) -> list[str]:
        return ['emote1', 'emote1', 'emote1']

    with patch(
        'tbot2.channel_gambling.actions.slots_actions.random_choices',
        mock_win_random_choices,
    ):
        result = await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet=100,
        )
        assert 'you WON 800 points' in result.message
        assert result.points == 900

    with patch(
        'tbot2.channel_gambling.actions.slots_actions.random_choices',
        mock_win_random_choices,
    ):
        result = await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet='all',
        )
        assert 'you WON 7200 points' in result.message
        assert result.points == 8100

    def mock_lose_random_choices(emotes: list[str]) -> list[str]:
        return ['emote1', 'emote2', 'emote3']

    with patch(
        'tbot2.channel_gambling.actions.slots_actions.random_choices',
        mock_lose_random_choices,
    ):
        result = await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet=100,
        )
        assert 'you lost 100 points' in result.message
        assert result.points == 8000

    with patch(
        'tbot2.channel_gambling.actions.slots_actions.random_choices',
        mock_lose_random_choices,
    ):
        result = await slots(
            channel_id=channel.id,
            provider='twitch',
            provider_viewer_id='test_chatter',
            bet='all',
        )
        assert 'you lost 8000 points' in result.message
        assert result.points == 0


if __name__ == '__main__':
    run_file(__file__)
