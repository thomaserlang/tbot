import random
from uuid import UUID

from tbot2.channel_points import get_channel_point_settings, get_points, inc_points
from tbot2.command import fill_from_dict
from tbot2.common import TProvider, convert_to_points

from ..actions.chatter_gambling_stats_actions import (
    inc_chatter_gambling_stats,
)
from ..actions.roulette_settings_actions import get_roulette_settings
from ..schemas.chatter_gambling_stats_schema import (
    ChatterGamblingStatsUpdate,
)
from ..schemas.roulette_schema import RouletteResult


async def roulette(
    *,
    channel_id: UUID,
    provider: TProvider,
    chatter_id: str,
    bet: int | str,
):
    point_settings = await get_channel_point_settings(channel_id=channel_id)
    settings = await get_roulette_settings(channel_id=channel_id)
    points = await get_points(
        channel_id=channel_id, provider=provider, chatter_id=chatter_id
    )

    bet = convert_to_points(bet, points.points)

    if bet < settings.min_bet:
        raise ValueError(f'Bet is too low, minimum is {settings.min_bet}')
    if settings.max_bet and bet > settings.max_bet:
        raise ValueError(f'Bet is too high, maximum is {settings.max_bet}')
    if bet > points.points:
        raise ValueError(f'Not enough {point_settings.points_name} to bet {bet}')

    won = random_int() < settings.win_chance
    new_points = await inc_points(
        channel_id=channel_id,
        provider=provider,
        chatter_id=chatter_id,
        points=bet if won else -bet,
    )

    message = ''
    if bet == points.points:
        message = settings.allin_win_message if won else settings.allin_lose_message
    else:
        message = settings.win_message if won else settings.lose_message

    if won:
        await inc_chatter_gambling_stats(
            channel_id=channel_id,
            provider=provider,
            chatter_id=chatter_id,
            data=ChatterGamblingStatsUpdate(roulette_wins=1),
        )

    return RouletteResult(
        won=won,
        bet=bet,
        points=points.points,
        points_name=point_settings.points_name,
        message=fill_from_dict(
            message,
            {
                'bet': bet,
                'points': new_points.points,
                'points_name': point_settings.points_name,
            },
        ),
    )


def random_int():
    return random.randint(1, 100)
