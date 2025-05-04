from tbot2.channel_chat_filters import create_permit
from tbot2.common import ChatMessageRequest, safe_username
from tbot2.twitch import lookup_twitch_user

from ..exceptions import CommandError, CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='twitch',
    vars=('permit_manager',),
)
async def permit_manager_var(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    if len(command.args) != 1:
        raise CommandSyntaxError(f'Syntax: !{command.name} <user>')
    chatter = await lookup_twitch_user(
        channel_id=chat_message.channel_id,
        login=safe_username(command.args[0]),
    )
    if not chatter:
        raise CommandError('User not found.')
    for_provider_viewer_id = chatter.id
    await create_permit(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        provider_viewer_id=for_provider_viewer_id,
        seconds=60,
    )
    vars[
        'permit_manager'
    ].value = f'@{chatter.display_name}, you have a permit for the next 60 seconds.'
