from tbot2.channel_points import get_channel_point_settings, inc_bulk_points, inc_points
from tbot2.common import ChatMessageRequest, safe_username
from tbot2.twitch import get_twitch_chatters, lookup_twitch_user

from ..exceptions import CommandError, CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='twitch', vars=('add_points',))
async def add_points_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) != 2:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user> <points>')

    try:
        points = int(command.args[1])
    except ValueError:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user> <points>') from None

    settings = await get_channel_point_settings(channel_id=chat_message.channel_id)

    if command.args[0] == 'all':
        total_chatters = 0
        async for chatters in await get_twitch_chatters(
            channel_id=chat_message.channel_id,
            broadcaster_id=chat_message.provider_id,
        ):
            await inc_bulk_points(
                channel_id=chat_message.channel_id,
                provider=chat_message.provider,
                provider_viewer_ids=[chatter.user_id for chatter in chatters],
                points=points,
            )
            total_chatters += len(chatters)
        vars[
            'add_points'
        ].value = f'Gave {points} {settings.points_name} to {total_chatters} chatters.'

    else:
        give_to_user = await lookup_twitch_user(
            channel_id=chat_message.channel_id, login=safe_username(command.args[0])
        )
        if not give_to_user:
            raise CommandError('User not found.')
        points = await inc_points(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            provider_viewer_id=give_to_user.id,
            points=points,
        )
        vars['add_points'].value = (
            f'{give_to_user.display_name} now has {points.points} '
            f'{settings.points_name}.'
        )
