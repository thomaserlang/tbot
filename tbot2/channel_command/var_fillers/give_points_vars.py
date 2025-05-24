from tbot2.channel_points import get_channel_point_settings, get_points, inc_points
from tbot2.common import (
    ChatMessageCreate,
    convert_to_points,
    safe_username,
)
from tbot2.contexts import get_session
from tbot2.twitch import lookup_twitch_user

from ..exceptions import CommandError, CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='twitch', vars=('give_points',))
async def give_points_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) != 2:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user> <points>')

    sender_points = await get_points(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        provider_viewer_id=chat_message.provider_viewer_id,
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

    if chat_message.provider_viewer_id == give_to_user.id:
        raise CommandError(f'You cannot give {settings.points_name} to yourself.')

    async with get_session() as session:
        await inc_points(
            session=session,
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            provider_viewer_id=chat_message.provider_viewer_id,
            points=-give_points,
        )

        await inc_points(
            session=session,
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            provider_viewer_id=give_to_user.id,
            points=give_points,
        )

    vars[
        'give_points'
    ].value = f'{chat_message.viewer_display_name} gave {give_points} '
    '{settings.points_name} to {give_to_user.display_name}.'
