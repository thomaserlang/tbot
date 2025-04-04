from typing import Literal

from tbot2.common import TScope

TimerPickMode = Literal[
    'order',
    'random',
]

TimerActiveMode = Literal[
    'always',
    'online',
    'offline',
]


class TimerScope(TScope):
    READ = 'channel_timer:read'
    WRITE = 'channel_timer:write'
