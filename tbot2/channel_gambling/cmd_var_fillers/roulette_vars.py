from tbot2.command import TCommand, TMessageVars, fills_vars
from tbot2.common import ChatMessage

from ..actions.roulette_actions import roulette


@fills_vars(provider='all', vars=('gamble_roulette',))
async def roulette_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
):
    result = await roulette(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=chat_message.chatter_id,
        bet=command.args[0],
    )
    vars['gamble_roulette'].value = result.message
