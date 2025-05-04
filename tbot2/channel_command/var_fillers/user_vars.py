from tbot2.common import ChatMessageRequest, safe_username

from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('user',),
)
async def user_vars(
    chat_message: ChatMessageRequest, command: TCommand, vars: MessageVars
) -> None:
    vars['user'].value = chat_message.viewer_display_name
    if command.args:
        vars['user'].value = safe_username(command.args[0])
