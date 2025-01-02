from tbot2.channel_gambling import roulette
from tbot2.command import Command, TMessageVars, fills_vars
from tbot2.common import ChatMessage


@fills_vars(provider='all', vars=('gamble_roulette',))
async def roulette_command(
    chat_message: ChatMessage, command: Command, vars: TMessageVars
):
    result = await roulette(
        channel_id=chat_message.channel_id,
        provider=chat_message.provider,
        chatter_id=chat_message.chatter_id,
        bet=command.args[0],
    )
    vars['gamble_roulette'].value = result.message
