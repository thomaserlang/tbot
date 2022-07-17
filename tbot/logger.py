import logging, logging.handlers, os
import sentry_sdk
from tbot import config
from tornado import log

class logger(object):

    @classmethod
    def set_logger(cls, filename, sentry_dsn=None):
        logger = logging.getLogger()
        logger.setLevel(config.data.logging.level.upper())

        format_ = log.LogFormatter(
            '[%(color)s%(levelname)s%(end_color)s %(asctime)s %(module)s:%(lineno)d]: %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        if config.data.logging.path and filename:
            channel = logging.handlers.RotatingFileHandler(
                filename=os.path.join(config.data.logging.path, filename),
                maxBytes=config.data.logging.max_size,
                backupCount=config.data.logging.num_backups
            )
            channel.setFormatter(format_)
            logger.addHandler(channel)
        else:# send to console instead of file
            channel = logging.StreamHandler()
            channel.setFormatter(format_)
            logger.addHandler(channel)

        if sentry_dsn:
            sentry_sdk.init(sentry_dsn)