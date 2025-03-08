from tbot2.command import Command, TMessageVars, fills_vars
from tbot2.common import ChatMessage

from ..actions.slots_actions import slots


@fills_vars(provider='all', vars=('gamble_slots',))
async def slots_vars(chat_message: ChatMessage, command: Command, vars: TMessageVars):
    result = await slots(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=chat_message.chatter_id,
        bet=command.args[0],
    )
    vars['gamble_slots'].value = result.message
