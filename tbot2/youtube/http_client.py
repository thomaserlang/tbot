import sys

from httpx import AsyncClient

from tbot2.common.utils.oauth_auth import ChannelProviderOAuth
from tbot2.config_settings import config

youtube_user_client = AsyncClient(
    base_url='https://www.googleapis.com/youtube/v3',
    headers={
        'Client-ID': config.youtube.client_id,
    },
    auth=ChannelProviderOAuth(
        provider='youtube',
        token_url='https://oauth2.googleapis.com/token',
        client_id=config.youtube.client_id,
        client_secret=config.youtube.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
    http2=True,
)
