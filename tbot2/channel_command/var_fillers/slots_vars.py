from tbot2.channel_gambling import slots
from tbot2.common import ChatMessage
from tbot2.exceptions import ErrorMessage

from ..exceptions import CommandSyntaxError
from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('gamble_slots',))
async def slots_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
) -> None:
    try:
        result = await slots(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            chatter_id=chat_message.chatter_id,
            bet=command.args[0],
        )
        vars['gamble_slots'].value = result.message
    except ErrorMessage as e:
        raise CommandSyntaxError(e) from e
