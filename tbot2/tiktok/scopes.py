from tbot2.common import channel_provider_scopes

channel_provider_scopes['tiktok'] = ','.join(
    {
        'user.info.basic',
        'user.info.profile',
    }
)
