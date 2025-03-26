from enum import Enum

from tbot2.common import TScope


class TChatFilterScope(TScope):
    READ = 'chat_filter:read'
    WRITE = 'chat_filter:write'


class TBannedTermType(str, Enum):
    phrase = 'phrase'
    re = 're'
