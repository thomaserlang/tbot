from enum import StrEnum

from tbot2.common import TScope


class TChatFilterScope(TScope):
    READ = 'chat_filter:read'
    WRITE = 'chat_filter:write'


class TBannedTermType(StrEnum):
    phrase = 'phrase'
    regex = 'regex'
