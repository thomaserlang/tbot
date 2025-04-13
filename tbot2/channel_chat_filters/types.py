from typing import Literal

from tbot2.common import Scope


class ChatFilterScope(Scope):
    READ = 'chat_filter:read'
    WRITE = 'chat_filter:write'


BannedTermType = Literal['phrase', 'regex']
