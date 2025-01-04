from tbot2.channel_points import (
    get_points_rank,
)
from tbot2.command import Command, TMessageVars, fills_vars
from tbot2.common import ChatMessage, TProvider, safe_username

from ..actions.twitch_lookup_users_action import lookup_twitch_user


@fills_vars(
    provider=TProvider.twitch,
    vars=(
        'points',
        'points_rank',
    ),
)
async def chatter_points(
    chat_message: ChatMessage, command: Command, vars: TMessageVars
):
    for_chatter_id = chat_message.chatter_id
    if len(command.args) > 0:
        chatter = await lookup_twitch_user(login=safe_username(command.args[0]))
        if not chatter:
            raise ValueError('User not found.')
        for_chatter_id = chatter.id

    points_rank = await get_points_rank(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=for_chatter_id,
    )

    if not points_rank:
        raise ValueError('No data on user.')

    vars['points'].value = points_rank.points
    vars['points_rank'].value = points_rank.rank
