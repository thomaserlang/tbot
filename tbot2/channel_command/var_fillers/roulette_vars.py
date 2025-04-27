from tbot2.channel_gambling import roulette
from tbot2.common import ChatMessage
from tbot2.common.exceptions import ErrorMessage

from ..exceptions import CommandSyntaxError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('gamble_roulette',))
async def roulette_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    try:
        result = await roulette(
            channel_id=chat_message.channel_id,
            provider=chat_message.provider,
            provider_viewer_id=chat_message.provider_viewer_id,
            bet=command.args[0],
        )
        vars['gamble_roulette'].value = result.message
    except ErrorMessage as e:
        raise CommandSyntaxError(e) from e
