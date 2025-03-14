import os
import sys
from typing import Literal

from pydantic import BaseModel
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict


class ConfigWebModel(BaseModel):
    port: int = 8001
    cookie_secret: str = ''
    name: str = 'TBot'
    base_url: str = 'https://botashell.com'


class ConfigTwitchModel(BaseModel):
    username: str = ''
    chat_token: str = ''
    client_id: str = ''
    client_secret: str = ''
    eventsub_host: str = 'https://api.twitch.tv'
    eventsub_secret: str = ''
    irc_host: str = 'irc.chat.twitch.tv'
    irc_port: int = 6697
    irc_use_ssl: bool = True
    irc_rate_limit: int = 80  # messages, every 30 second
    check_channels_every: int = 60  # seconds
    check_timers_every: int = 30  # seconds
    delay_offline: int = 0  # seconds
    # Only reset streams in a row if the stream was longer than `stream_min_length`.
    stream_min_length: int = 1800  # seconds
    pubsub_url: str = 'wss://pubsub-edge.twitch.tv'
    request_scope: list[str] = [
        'channel_editor',
        'bits:read',
        'clips:edit',
        'moderation:read',
        'channel:moderate',
        'channel:edit:commercial',
        'channel:manage:polls',
        'channel:manage:predictions',
        'channel:manage:redemptions',
        'channel:manage:videos',
        'channel:manage:broadcast',
        'channel:read:goals',
        'channel:read:hype_train',
        'channel:read:polls',
        'channel:read:predictions',
        'channel:read:redemptions',
        'channel:read:subscriptions',
        'channel:bot',
        'moderator:manage:banned_users',
        'moderator:read:chatters',
        'channel:read:vips',
        'moderator:manage:chat_messages',
        'moderator:manage:chat_settings',
        'moderator:manage:announcements',
        'chat:edit',
        'chat:read',
        'moderator:read:followers',
        'user:bot',
    ]


class ConfigGoogleModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigGithubModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigYoutubeModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''
    twitch_bot_channel_id: str = ''


class ConfigDiscordModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''
    permissions: int = 470019158
    token: str | None = None
    user_token: str | None = None
    twitch_sync_every: int = 3600  # seconds


class ConfigSpotifyConfig(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigLoggingModel(BaseModel):
    level: Literal['notset', 'debug', 'info', 'warn', 'error', 'critical'] = 'warn'
    path: str | None = None
    max_size: int = 100 * 1000 * 1000  # ~ 95 mb
    num_backups: int = 10


class ConfigMySQLModel(BaseModel):
    drivername: str = 'mariadb+asyncmy'
    host: str = '127.0.0.1'
    port: int = 3306
    user: str = 'root'
    password: str | None = None
    database: str = 'tbot'


class ConfigRedisModel(BaseModel):
    host: str = '127.0.0.1'
    port: int = 6379
    pool_min_size: int = 5
    pool_max_size: int = 20
    password: str | None = None
    db: int = 0
    queue_name: str = 'tbot'


def get_config_path():
    path = os.environ.get('TBOT__CONFIG', None) or os.environ.get('TBOT_CONFIG', None)
    if not path:
        default_paths = (
            os.path.abspath(os.path.join(os.path.dirname(__file__), '../tbot.yaml')),
            '~/tbot.yaml',
            '/etc/tbot/tbot.yaml',
            '/etc/tbot.yaml',
            '/etc/tbot/config.yml',
        )

        if 'pytest' in sys.modules:
            default_paths = (
                os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '../tbot_test.yaml')
                ),
            )
        for p in default_paths:
            p = os.path.expanduser(p)
            if os.path.isfile(p):
                path = p
                break
    if path:
        import logging

        logging.basicConfig(level=logging.INFO, format='%(message)s')
        logging.info(f'Using config: {path}')
    else:
        raise Exception('No config file specified')
    return path


class ConfigSettings(BaseYamlSettings):
    model_config = YamlSettingsConfigDict(
        env_prefix='tbot__',
        env_nested_delimiter='__',
        validate_assignment=True,
        case_sensitive=False,
        extra='forbid',
        yaml_files=get_config_path(),
        yaml_reload=False,
    )

    debug: bool = False
    sentry_dsn: str | None = None
    web: ConfigWebModel = ConfigWebModel()
    twitch: ConfigTwitchModel = ConfigTwitchModel()
    discord: ConfigDiscordModel = ConfigDiscordModel()
    google: ConfigGoogleModel = ConfigGoogleModel()
    github: ConfigGithubModel = ConfigGithubModel()
    youtube: ConfigYoutubeModel = ConfigYoutubeModel()
    spotify: ConfigSpotifyConfig = ConfigSpotifyConfig()
    logging: ConfigLoggingModel = ConfigLoggingModel()
    mysql: ConfigMySQLModel = ConfigMySQLModel()
    redis: ConfigRedisModel = ConfigRedisModel()
    openweathermap_apikey: str | None = None
    faceit_apikey: str | None = None
    lol_apikey: str | None = None
    tft_apikey: str | None = None
    rtmp_keys: list[str] = []


try:
    config = ConfigSettings()
except Exception as e:
    sys.exit(str(e))
