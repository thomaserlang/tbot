import os
import sys
from pathlib import Path
from typing import Literal
from uuid import UUID

from loguru import logger
from pydantic import AnyHttpUrl, BaseModel
from yaml_settings_pydantic import BaseYamlSettings, YamlSettingsConfigDict


class ConfigTwitchModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''
    eventsub_secret: str = ''
    eventsub_callback_base_url: AnyHttpUrl | None = None


class ConfigYoutubeModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigDiscordModel(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigSpotifyConfig(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigTiktokConfig(BaseModel):
    client_id: str = ''
    client_secret: str = ''


class ConfigLoggingModel(BaseModel):
    level: Literal['notset', 'trace', 'debug', 'info', 'warn', 'error', 'critical'] = (
        'info'
    )
    path: str | None = None
    max_size: int = 100 * 1000 * 1000  # ~ 95 mb
    num_backups: int = 10


class ConfigDBModel(BaseModel):
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


class ConfigElasticsearchModel(BaseModel):
    host: str = 'http://localhost:9200/'
    user: str = ''
    password: str = ''
    verify_certs: bool = False


def get_config_path() -> Path:
    path: Path | None = None
    if os.environ.get('TBOT__CONFIG', None):
        path = Path(os.environ['TBOT__CONFIG'])
    if os.environ.get('TBOT_CONFIG', None):
        path = Path(os.environ['TBOT_CONFIG'])

    if not path:
        default_paths = (
            Path(__file__).parent / '../tbot.yaml',
            Path('~/tbot.yaml'),
            Path('/etc/tbot/tbot.yaml'),
            Path('/etc/tbot.yaml'),
            Path('/etc/tbot/config.yml'),
        )

        if 'pytest' in sys.modules:
            default_paths = (Path(__file__).parent / '../tbot_test.yaml',)

        for p in default_paths:
            if p.exists():
                path = p
                break
    if not path:
        raise Exception('No config file specified. Set it with `TBOT__CONFIG` env var.')

    path = path.expanduser()
    if not path.exists():
        raise Exception(f'Config file does not exist: {path}')

    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format='<blue>{message}</blue>',
    )
    logger.info(f'Config: {path}')
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
    port: int = 8001
    secret: str = ''
    base_url: AnyHttpUrl = AnyHttpUrl('https://synchra.net')
    twitch: ConfigTwitchModel = ConfigTwitchModel()
    discord: ConfigDiscordModel = ConfigDiscordModel()
    youtube: ConfigYoutubeModel = ConfigYoutubeModel()
    spotify: ConfigSpotifyConfig = ConfigSpotifyConfig()
    tiktok: ConfigTiktokConfig = ConfigTiktokConfig()
    logging: ConfigLoggingModel = ConfigLoggingModel()
    db: ConfigDBModel = ConfigDBModel()
    elasticsearch: ConfigElasticsearchModel = ConfigElasticsearchModel()
    redis: ConfigRedisModel = ConfigRedisModel()
    openweathermap_apikey: str | None = None
    faceit_apikey: str | None = None
    global_admins: set[UUID] = set()


try:
    config = ConfigSettings()
except Exception as e:
    sys.exit(str(e))
