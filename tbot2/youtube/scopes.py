from tbot2.common import bot_provider_scopes, channel_provider_scopes

bot_provider_scopes['youtube'] = ' '.join(
    {
        'https://www.googleapis.com/auth/youtube',
    }
)

channel_provider_scopes['youtube'] = ' '.join(
    {
        'https://www.googleapis.com/auth/youtube',
    }
)
