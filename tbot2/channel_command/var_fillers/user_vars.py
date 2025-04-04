from tbot2.common import ChatMessage

from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('user',),
)
async def user_vars(chat_message: ChatMessage, command: TCommand, vars: TMessageVars):
    vars['user'].value = chat_message.chatter_display_name
    if command.args:
        vars['user'].value = command.args[0]
