import pytz

from tbot2.common import ChatMessage, datetime_now

from ..types import Command, TMessageVars
from ..var_filler import fills_vars


@fills_vars(
    provider='all',
    vars=('time',),
)
async def time_vars(chat_message: ChatMessage, command: Command, vars: TMessageVars):
    if not vars['time'].args:
        raise ValueError(
            'A timezone must be specified with time. Example {time Europe/Copenhagen}'
        )
    if vars['time'].args[0] not in pytz.all_timezones:
        raise ValueError(
            'Invalid timezone. Valid list: https://docs.botashell.com/vars/time'
        )
    dt = pytz.utc.localize(
        datetime_now(),
    ).astimezone(pytz.timezone(vars['time'].args[0]))

    vars['time'].value = dt.strftime('%H:%M')
