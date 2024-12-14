import humanize.time

from tbot2.command import Command, TMessageVars, VarFillError, fills_vars
from tbot2.common import ChatMessage, datetime_now

from ..actions.twitch_lookup_users_action import twitch_lookup_users


@fills_vars(
    provider='twitch', vars=('accountage', 'accountage_date', 'accountage_datetime')
)
async def accountage(chat_message: ChatMessage, command: Command, vars: TMessageVars):
    created_at = await twitch_accountage(chat_message, command)

    vars['accountage'].value = (
        humanize.time.precisedelta(
            datetime_now() - created_at,
        )
        + ' ago'
    )
    vars['accountage_date'].value = humanize.naturaldate(created_at)
    vars['accountage_datetime'].value = created_at.strftime('%Y-%m-%d %H:%M:%S UTC')


async def twitch_accountage(chat_message: ChatMessage, command: Command):
    users = await twitch_lookup_users(
        logins=[command.args[0]] if command.args else [],
        user_ids=[chat_message.chatter_id] if not command.args else [],
    )

    if not users:
        raise VarFillError('Unknown user')

    return users[0].created_at
