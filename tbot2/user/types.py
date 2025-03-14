from tbot2.common import TScope


class TUserScope(TScope):
    READ = 'user:read'
    WRITE = 'user:write'
    ADMIN = 'user:admin'