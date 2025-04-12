from random import randint

from tbot2.common import ChatMessage

from ..exceptions import CommandSyntaxError
from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('randint',),
)
async def randint_vars(
    chat_message: ChatMessage, command: TCommand, vars: TMessageVars
) -> None:
    from_ = 1
    to = 100

    if vars['randint'].args:
        num_args = [int(arg) for arg in vars['randint'].args if arg.isdigit()]
        if num_args:
            from_ = num_args[0]
            if len(num_args) > 1:
                to = num_args[1]

    num_args = [int(arg) for arg in command.args if arg.isdigit()]
    if num_args:
        to = num_args[0]
        if len(num_args) > 1:
            from_ = num_args[1]

    if to <= from_:
        raise CommandSyntaxError('First argument must be lower than the second')

    vars['randint'].value = randint(from_, to)
