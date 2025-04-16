from tbot2.channel_gambling import get_chatter_gambling_stats
from tbot2.common import ChatMessage, safe_username
from tbot2.twitch import lookup_twitch_user

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=(
        'gambling_stats.slots_wins',
        'gambling_stats.slots_loses',
        'gambling_stats.slots_total_games',
        'gambling_stats.slots_win_percent',
        'gambling_stats.roulette_wins',
        'gambling_stats.roulette_loses',
        'gambling_stats.roulette_total_games',
        'gambling_stats.roulette_win_percent',
    ),
)
async def gambling_stats(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    for_provider_viewer_id = chat_message.provider_viewer_id
    if len(command.args) > 0:
        chatter = await lookup_twitch_user(
            channel_id=chat_message.channel_id,
            login=safe_username(command.args[0]),
        )
        if not chatter:
            raise CommandError('User not found.')
        for_provider_viewer_id = chatter.id

    stats = await get_chatter_gambling_stats(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        provider_viewer_id=for_provider_viewer_id,
    )

    vars['gambling_stats.slots_wins'].value = stats.slots_wins
    vars['gambling_stats.slots_loses'].value = stats.slots_losses
    total_slots_games = stats.slots_wins + stats.slots_losses
    vars['gambling_stats.slots_total_games'].value = total_slots_games
    vars['gambling_stats.slots_win_percent'].value = (
        f'{stats.slots_wins / total_slots_games:.1%}' if total_slots_games > 0 else '0%'
    )
    vars['gambling_stats.roulette_wins'].value = stats.roulette_wins
    vars['gambling_stats.roulette_loses'].value = stats.roulette_losses
    total_roulette_games = stats.roulette_wins + stats.roulette_losses
    vars['gambling_stats.roulette_total_games'].value = total_roulette_games
    vars['gambling_stats.roulette_win_percent'].value = (
        f'{stats.roulette_wins / total_roulette_games:.1%}'
        if total_roulette_games > 0
        else '0%'
    )
