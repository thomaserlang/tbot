from tbot2.common import ChatMessage

from ..types import Command, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('sender',),
)
async def sender_vars(chat_message: ChatMessage, command: Command, vars: TMessageVars):
    vars['sender'].value = chat_message.chatter_display_name
