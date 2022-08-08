import os, yaml
from typing import List, Optional, Literal
from pydantic import BaseModel, DirectoryPath

class ConfigWebModel(BaseModel):
    port = 8001
    cookie_secret: Optional[str]
    name = 'TBot'
    base_url = 'https://botashell.com'


class ConfigTwitchModel(BaseModel):
    username: Optional[str]
    chat_token: Optional[str]
    client_id: Optional[str]
    client_secret: Optional[str]
    eventsub_host = 'https://api.twitch.tv'
    eventsub_secret: Optional[str]
    irc_host = 'irc.chat.twitch.tv'
    irc_port = 6697
    irc_use_ssl = True
    irc_rate_limit = 80 # messages, every 30 second
    check_channels_every = 60 # seconds
    check_timers_every = 30 # seconds
    delay_offline = 0 # seconds
    # Only reset streams in a row if the stream was longer than `stream_min_length`.
    stream_min_length = 1800 # seconds
    pubsub_url = 'wss://pubsub-edge.twitch.tv'
    request_scope = ['channel_editor', 'bits:read', 'clips:edit', 'moderation:read',
                    'channel:moderate', 'channel:edit:commercial', 'channel:manage:polls',
                    'channel:manage:predictions', 'channel:manage:redemptions',
                    'channel:manage:videos', 'channel:manage:broadcast',
                    'channel:read:goals', 'channel:read:hype_train', 'channel:read:polls',
                    'channel:read:predictions', 'channel:read:redemptions', 'channel:read:subscriptions',]


class ConfigDiscordModel(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]
    permissions = 470019158
    token: Optional[str]
    bot = True
    user_token: Optional[str]
    twitch_sync_every = 3600 # seconds


class ConfigSpotifyConfig(BaseModel):
    client_id: Optional[str]
    client_secret: Optional[str]    


class ConfigLoggingModel(BaseModel):
    level: Literal['notset', 'debug', 'info', 'warn', 'error', 'critical'] = 'warn'
    path: Optional[DirectoryPath]
    max_size: int = 100 * 1000 * 1000 # ~ 95 mb
    num_backups = 10
    

class ConfigMySQLModel(BaseModel):
    host = '127.0.0.1'
    port = 3306
    user = 'root'
    password: Optional[str]
    database = 'tbot'



class ConfigRedisModel(BaseModel):
    host = '127.0.0.1'
    port = 6379
    pool_min_size = 5
    pool_max_size = 20



class ConfigModel(BaseModel):
    debug = False
    sentry_dsn: Optional[str]
    web = ConfigWebModel()
    twitch = ConfigTwitchModel()
    discord = ConfigDiscordModel()
    spotify = ConfigSpotifyConfig()
    logging = ConfigLoggingModel()
    mysql = ConfigMySQLModel()
    redis = ConfigRedisModel()
    openweathermap_apikey: Optional[str]
    faceit_apikey: Optional[str]
    lol_apikey: Optional[str]
    tft_apikey: Optional[str]
    rtmp_keys: List[str] = []


class Config:
    def __init__(self):
        self.data = ConfigModel()
config = Config()

def load(path=None):
    default_paths = [
        '~/tbot.yaml',
        './tbot.yaml',
        '../tbot.yaml',
        '/etc/tbot/tbot.yaml',
        '/etc/tbot.yaml',
        '/etc/tbot/tbot.yml',
        '/etc/tbot.yml',
    ]
    if not path:
        path = os.environ.get('TBOT_CONFIG', None)
        if not path:
            for p in default_paths:
                p = os.path.expanduser(p)
                if os.path.isfile(p):
                    path = p
                    break
    if not path:
        return
    if not os.path.isfile(path):
        raise Exception('Config: "{}" could not be found.'.format(path))
    with open(path) as f:
        data = yaml.load(f, Loader=yaml.SafeLoader)
        config.data = ConfigModel(**data)