from tbot2.common import Scope


class ChannelProviderScope(Scope):
    WRITE = 'channel_providers:write'
    READ = 'channel_providers:read'
    CHAT_MODERATION = 'channel_providers:chat_moderation'
