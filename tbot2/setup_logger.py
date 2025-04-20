import sys

from loguru import logger

from tbot2.config_settings import config


def setup_logger() -> None:
    logger.remove()
    format = '<green>{time}</green> | <level>{level}</level> | {message} | {extra}'
    if config.debug:
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
