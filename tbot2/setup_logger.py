import sys

import sentry_sdk
from loguru import logger

from tbot2.config_settings import config

logger.remove()

sentry_sdk.init(
    dsn=config.sentry_dsn,
    send_default_pii=True,
)
format = (
    '<green>{time:HH:mm:ss.SSS}</green> | '
    '<level>{level}</level> | '
    '{message} | {extra} | '
    '<light-blue>{module}.{function}:{line}</light-blue>'
)
logger.add(
    sys.stderr,
    colorize=True,
    format=format,
    level=config.logging.level.upper(),
)
