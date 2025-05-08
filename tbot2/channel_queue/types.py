from tbot2.common import Scope


class ChannelQueueScope(Scope):
    READ = 'channel_viewer_queue:read'
    WRITE = 'channel_viewer_queue:write'
