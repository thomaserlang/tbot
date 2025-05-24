from datetime import UTC

import humanize
from dateutil.parser import parse

from tbot2.common import ChatMessageCreate, datetime_now

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('countdown',))
async def countdown_vars(
    chat_message: ChatMessageCreate, command: TCommand, vars: MessageVars
) -> None:
    try:
        dt = parse(' '.join(vars['countdown'].args))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)

        vars['countdown'].value = humanize.precisedelta(datetime_now() - dt)
    except ValueError as e:
        raise CommandError(
            f'Invalid date format: "{" ".join(vars["countdown"].args)}". '
            'Use ISO 8601 format.'
        ) from e
