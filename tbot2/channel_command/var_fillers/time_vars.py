import pytz

from tbot2.common import ChatMessage, datetime_now

from ..exceptions import CommandError
from ..types import MessageVars, TCommand
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('time',),
)
async def time_vars(
    chat_message: ChatMessage, command: TCommand, vars: MessageVars
) -> None:
    if not vars['time'].args:
        raise CommandError(
            'A timezone must be specified with time. Example {time Europe/Copenhagen}'
        )
    if vars['time'].args[0] not in pytz.all_timezones:
        raise CommandError(
            'Invalid timezone. Valid list: https://docs.botashell.com/docs/time'
        )
    dt = datetime_now().astimezone(pytz.timezone(vars['time'].args[0]))

    vars['time'].value = dt.strftime('%H:%M')
