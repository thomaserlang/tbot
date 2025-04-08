from tbot2.channel_command import (
    CommandError,
    CommandSyntaxError,
    TCommand,
    TMessageVars,
    fills_vars,
)
from tbot2.channel_points import get_channel_point_settings, get_points, inc_points
from tbot2.common import ChatMessage, TProvider, convert_to_points, safe_username
from tbot2.contexts import get_session

from ..actions.twitch_lookup_users_action import lookup_twitch_user


@fills_vars(provider=TProvider.twitch, vars=('give_points',))
async def give_points_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    if len(command.args) != 2:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user> <points>')

    sender_points = await get_points(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=chat_message.chatter_id,
    )

    try:
        give_points = convert_to_points(command.args[1], sender_points.points)
    except ValueError:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user> <points>') from None

    settings = await get_channel_point_settings(channel_id=chat_message.channel_id)

    give_to_user = await lookup_twitch_user(
        channel_id=chat_message.channel_id,
        login=safe_username(command.args[0]),
    )
    if not give_to_user:
        raise CommandError('User not found.')

    if give_points > sender_points.points:
        raise CommandError(
            f'You only have {sender_points.points} {settings.points_name}.'
        )
    if give_points < 1:
        raise CommandError(f'You must give at least 1 {settings.points_name}.')

    if chat_message.chatter_id == give_to_user.id:
        raise CommandError(f'You cannot give {settings.points_name} to yourself.')

    async with get_session() as session:
        await inc_points(
            session=session,
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=chat_message.chatter_id,
            points=-give_points,
        )

        await inc_points(
            session=session,
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=give_to_user.id,
            points=give_points,
        )

    vars[
        'give_points'
    ].value = f'{chat_message.chatter_display_name} gave {give_points} '
    '{settings.points_name} to {give_to_user.display_name}.'
