import humanize.time

from tbot2.channel_command import CommandError, TCommand, TMessageVars, fills_vars
from tbot2.common import ChatMessage, TProvider, datetime_now

from ..actions.twitch_channel_follower_action import twitch_channel_follower
from ..actions.twitch_lookup_users_action import (
    lookup_twitch_users,
)


@fills_vars(
    provider=TProvider.twitch,
    vars=('followage', 'followage_date', 'followage_datetime'),
)
async def followage_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    followed_at = await twitch_followed_at(chat_message=chat_message, command=command)

    vars['followage'].value = (
        humanize.time.precisedelta(
            datetime_now() - followed_at,
        )
        + ' ago'
    )
    vars['followage_date'].value = humanize.naturaldate(followed_at)
    vars['followage_datetime'].value = followed_at.strftime('%Y-%m-%d %H:%M:%S UTC')


async def twitch_followed_at(chat_message: ChatMessage, command: TCommand):
    user_id = chat_message.chatter_id
    display_name = chat_message.chatter_display_name
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
