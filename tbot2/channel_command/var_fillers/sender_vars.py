from tbot2.common import ChatMessageCreate

from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('sender',),
)
async def sender_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    vars['sender'].value = chat_message.viewer_display_name
