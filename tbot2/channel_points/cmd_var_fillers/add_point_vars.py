from tbot2.channel_points import get_channel_point_settings, inc_bulk_points, inc_points
from tbot2.command import Command, TMessageVars, fills_vars
from tbot2.common import ChatMessage, TProvider, safe_username
from tbot2.twitch import get_twitch_chatters, twitch_lookup_user


@fills_vars(provider=TProvider.twitch, vars=('add_points',))
async def add_points_vars(
    chat_message: ChatMessage, command: Command, vars: TMessageVars
):
    if len(command.args) != 2:
        raise ValueError(f'Syntax: !{command.name} <user> <points>')

    try:
        points = int(command.args[1])
    except ValueError:
        raise ValueError(f'Syntax: !{command.name} <user> <points>')

    settings = await get_channel_point_settings(channel_id=chat_message.channel_id)

    if command.args[0] == 'all':
        chatters = await get_twitch_chatters(
            broadcaster_id=chat_message.provider_id,
        )
        await inc_bulk_points(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_ids=[chatter.user_id for chatter in chatters],
            points=points,
        )
        vars[
            'add_points'
        ].value = f'Gave {points} {settings.points_name} to {len(chatters)} chatters.'
    else:
        give_to_user = await twitch_lookup_user(login=safe_username(command.args[0]))
        if not give_to_user:
            raise ValueError('User not found.')
        points = await inc_points(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=give_to_user.id,
            points=points,
        )
        vars[
            'add_points'
        ].value = f'{give_to_user.display_name} now has {points.points} {settings.points_name}.'
