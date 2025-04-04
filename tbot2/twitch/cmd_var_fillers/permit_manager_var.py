from tbot2.channel_chat_filters import create_permit
from tbot2.channel_command.types import TCommand, TMessageVars
from tbot2.channel_command.var_filler import fills_vars
from tbot2.common import ChatMessage, TProvider, safe_username

from ..actions.twitch_lookup_users_action import lookup_twitch_user


@fills_vars(
    provider=TProvider.twitch,
    vars=('permit',),
)
async def permit_manager_var(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    if len(command.args) != 1:
        raise ValueError(f'Syntax: !{command.name} <user>')
    chatter = await lookup_twitch_user(
        channel_id=chat_message.channel_id,
        login=safe_username(command.args[0]),
    )
    if not chatter:
        raise ValueError('User not found.')
    for_chatter_id = chatter.id
    await create_permit(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=for_chatter_id,
        seconds=60,
    )
    vars[
        'permit'
    ].value = f'@{chatter.display_name}, you have a permit for the next 60 seconds.'
