from datetime import timezone

import humanize
from dateutil.parser import parse

from tbot2.common import ChatMessage, datetime_now

from ..exceptions import VarFillError
from ..types import Command, TMessageVars
from ..var_filler import fills_vars


@fills_vars(provider='all', vars=('countdown',))
async def countdown_vars(
    chat_message: ChatMessage, command: Command, vars: TMessageVars
):
    try:
        dt = parse(' '.join(vars['countdown'].args))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        vars['countdown'].value = humanize.precisedelta(datetime_now() - dt)
    except ValueError:
        raise VarFillError(
            f'Invalid date format: "{" ".join(vars["countdown"].args)}". Use ISO 8601 format.'
        )
