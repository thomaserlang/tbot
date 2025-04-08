import humanize.time

from tbot2.channel_command import CommandError, TCommand, TMessageVars, fills_vars
from tbot2.common import ChatMessage, TProvider, datetime_now

from ..actions.twitch_lookup_users_action import lookup_twitch_users


@fills_vars(
    provider=TProvider.twitch,
    vars=('accountage', 'accountage_date', 'accountage_datetime'),
)
async def accountage_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    created_at = await twitch_accountage(chat_message, command)

    vars['accountage'].value = (
        humanize.time.precisedelta(
            datetime_now() - created_at,
        )
        + ' ago'
    )
    vars['accountage_date'].value = humanize.naturaldate(created_at)
    vars['accountage_datetime'].value = created_at.strftime('%Y-%m-%d %H:%M:%S UTC')


async def twitch_accountage(chat_message: ChatMessage, command: TCommand):
    users = await lookup_twitch_users(
        channel_id=chat_message.channel_id,
        logins=[command.args[0]] if command.args else [],
        user_ids=[chat_message.chatter_id] if not command.args else [],
    )

    if not users:
        raise CommandError('Unknown user')

    return users[0].created_at
