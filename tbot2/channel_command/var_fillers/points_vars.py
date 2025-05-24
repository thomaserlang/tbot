from tbot2.channel_points import get_points_rank, get_total_point_users
from tbot2.common import ChatMessageCreate, safe_username
from tbot2.twitch import lookup_twitch_user

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('points', 'points_rank', 'total_point_users'),
)
async def chatter_point_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
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

    points_rank = await get_points_rank(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        provider_viewer_id=for_provider_viewer_id,
    )

    if not points_rank:
        raise CommandError('No data on user.')

    vars['points'].value = points_rank.points
    vars['points_rank'].value = points_rank.rank
    vars['total_point_users'].value = await get_total_point_users(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
    )
