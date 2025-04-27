from tbot2.common import Scope


class TUserScope(Scope):
    READ = 'user:read'
    WRITE = 'user:write'
    ADMIN = 'user:admin'