from tbot2.common import bot_provider_scopes, channel_provider_scopes

bot_provider_scopes['twitch'] = ' '.join(
    {
        'user:bot',
        'user:write:chat',
        'user:read:chat',
        'moderator:manage:automod',
        'moderator:manage:announcements',
        'moderator:manage:chat_messages',
        'moderator:manage:banned_users',
        'moderator:manage:warnings',
        'channel:moderate',
    }
)
channel_provider_scopes['twitch'] = ' '.join(
    {
        'channel:moderate',
        'channel:edit:commercial',
        'channel:manage:polls',
        'channel:manage:predictions',
        'channel:manage:redemptions',
        'channel:manage:broadcast',
        'channel:read:goals',
        'channel:read:hype_train',
        'channel:read:polls',
        'channel:read:predictions',
        'channel:read:redemptions',
        'channel:read:subscriptions',
        'moderator:read:banned_users',
        'moderator:manage:banned_users',
        'moderator:read:chatters',
        'moderator:manage:chat_messages',
        'moderator:manage:chat_settings',
        'moderator:manage:warnings',
        'moderation:read',
        'moderator:read:followers',
        'moderator:read:blocked_terms',
        'moderator:read:unban_requests',
        'moderator:read:moderators',
        'moderator:read:vips',
        'bits:read',
        'channel:bot',
        'channel:manage:moderators',
    }
)
