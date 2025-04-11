import sys

from httpx import AsyncClient

from tbot2.common import TProvider
from tbot2.common.utils.oauth_auth import ChannelProviderOAuth
from tbot2.config_settings import config

spotify_client = AsyncClient(
    base_url='https://api.spotify.com/v1',
    auth=ChannelProviderOAuth(
        provider=TProvider.spotify,
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
)
