import sys

from httpx import AsyncClient

from tbot2.common.utils.httpx_retry import retry_transport
from tbot2.common.utils.oauth_auth import ChannelProviderOAuthHelper
from tbot2.config_settings import config

spotify_client = AsyncClient(
    base_url='https://api.spotify.com/v1',
    auth=ChannelProviderOAuthHelper(
        provider='spotify',
        token_url='https://accounts.spotify.com/api/token',
        client_id=config.spotify.client_id,
        client_secret=config.spotify.client_secret,
    )
    if 'pytest' not in sys.modules
    else None,
    headers={
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
    transport=retry_transport,
    http2=True,
)
