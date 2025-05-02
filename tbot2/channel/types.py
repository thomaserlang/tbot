from tbot2.common import Scope


class ChannelScope(Scope):
    READ = 'channel:read'
    WRITE = 'channel:write'
    DELETE = 'channel:delete'
