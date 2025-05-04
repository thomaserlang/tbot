import humanize.time

from tbot2.common import ChatMessageRequest, datetime_now
from tbot2.twitch import lookup_twitch_users

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('accountage', 'accountage_date', 'accountage_datetime'),
)
async def accountage_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    users = await lookup_twitch_users(
        channel_id=chat_message.channel_id,
        logins=[command.args[0]] if command.args else [],
        user_ids=[chat_message.provider_viewer_id] if not command.args else [],
    )

    if not users:
        raise CommandError('Unknown user')
    created_at = users[0].created_at

    vars['accountage'].value = (
        humanize.time.precisedelta(
            datetime_now() - created_at,
        )
        + ' ago'
    )
    vars['accountage_date'].value = humanize.naturaldate(created_at)
    vars['accountage_datetime'].value = created_at.strftime('%Y-%m-%d %H:%M:%S UTC')
