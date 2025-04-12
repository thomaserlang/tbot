from tbot2.common import ChatMessage

from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('sender',),
)
async def sender_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
) -> None:
    vars['sender'].value = chat_message.chatter_display_name
