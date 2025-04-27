import math
import random
from uuid import UUID

from tbot2.channel_points import get_channel_point_settings, get_points, inc_points
from tbot2.common import Provider, convert_to_points
from tbot2.common.exceptions import ErrorMessage
from tbot2.common.utils.fill_from_dict import fill_from_dict

from ..actions.slots_settings_actions import get_slots_settings
from ..schemas.slots_schema import SlotsResult


async def slots(
    *,
    channel_id: UUID,
    provider: Provider,
    provider_viewer_id: str,
    bet: int | str,
) -> SlotsResult:
    point_settings = await get_channel_point_settings(channel_id=channel_id)
    settings = await get_slots_settings(channel_id=channel_id)
    points = await get_points(
        channel_id=channel_id, provider=provider, provider_viewer_id=provider_viewer_id
    )

    bet = convert_to_points(bet, points.points)

    if bet < settings.min_bet:
        raise ErrorMessage(f'Bet is too low, minimum is {settings.min_bet}')
    if settings.max_bet and bet > settings.max_bet:
        raise ErrorMessage(f'Bet is too high, maximum is {settings.max_bet}')
    if bet > points.points:
        raise ErrorMessage(f'Not enough {point_settings.points_name} to bet {bet}')

    if settings.emote_pool_size > len(settings.emotes):
        raise ErrorMessage('Not enough emotes in the pool')

    emotes = settings.emotes.copy()
    random.shuffle(emotes)
    emotes = random_choices(emotes[: settings.emote_pool_size])
    won = len(set(emotes)) == 1
    chance = (len(emotes) / (len(emotes) ** 3)) * 100
    multiplier = math.floor(settings.payout_percent / chance) or 1
    new_points = await inc_points(
        channel_id=channel_id,
        provider=provider,
        provider_viewer_id=provider_viewer_id,
        points=bet * multiplier if won else -bet,
    )

    message = ''
    if bet == points.points:
        message = settings.allin_win_message if won else settings.allin_lose_message
    else:
        message = settings.win_message if won else settings.lose_message

    return SlotsResult(
        won=won,
        bet=bet,
        emotes=emotes,
        points=new_points.points,
        points_name=point_settings.points_name,
        message=fill_from_dict(
            message,
            {
                'bet': bet * multiplier if won else bet,
                'points': new_points.points,
                'points_name': point_settings.points_name,
                'emotes': ' | '.join(emotes),
            },
        ),
    )


def random_choices(emotes: list[str]) -> list[str]:
    return random.choices(emotes, k=3)
