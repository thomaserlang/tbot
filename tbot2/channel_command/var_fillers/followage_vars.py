from datetime import datetime

import humanize.time

from tbot2.common import ChatMessageRequest, datetime_now
from tbot2.twitch import lookup_twitch_users, twitch_channel_follower

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('followage', 'followage_date', 'followage_datetime'),
)
async def followage_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    followed_at = await twitch_followed_at(chat_message=chat_message, command=command)

    vars['followage'].value = humanize.time.precisedelta(
        datetime_now() - followed_at, format='%0.0f', minimum_unit='days'
    )
    vars['followage_date'].value = humanize.naturaldate(followed_at)
    vars['followage_datetime'].value = followed_at.strftime('%Y-%m-%d %H:%M:%S UTC')


async def twitch_followed_at(chat_message: ChatMessageRequest, command: TCommand) -> datetime:
    user_id = chat_message.provider_viewer_id
    display_name = chat_message.viewer_display_name
    if command.args:
        user = await lookup_twitch_users(
            channel_id=chat_message.channel_id,
            logins=[command.args[0]],
        )
        if not user:
            raise CommandError(f'User {command.args[0]} not found.')
        user_id = user[0].id
        display_name = user[0].display_name

    follower = await twitch_channel_follower(
        channel_id=chat_message.channel_id,
        user_id=user_id,
        broadcaster_id=chat_message.provider_id,
    )
    if not follower:
        raise CommandError(f'{display_name} is not following.')

    return follower.followed_at
