from typing import Literal

from tbot2.common import Scope

TimerPickMode = Literal[
    'order',
    'random',
]

TimerActiveMode = Literal[
    'always',
    'online',
    'offline',
]


class TimerScope(Scope):
    READ = 'channel_timer:read'
    WRITE = 'channel_timer:write'
