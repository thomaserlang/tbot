import datetime
import logging, logging.handlers, os, sentry_sdk
from tbot import config
from tornado import log as tornadolog

logger = logging.getLogger('tbot')

logging.getLogger('urllib3').setLevel(logging.ERROR)

def set_logger(filename, to_sentry=True):
    logger.setLevel(config.data.logging.level.upper())
    glogger = logging.getLogger()
    glogger.handlers = []

    logging.Formatter.formatTime = (lambda self, record, datefmt=None: datetime.datetime.fromtimestamp(record.created, datetime.timezone.utc).astimezone().isoformat(sep="T",timespec="milliseconds"))
    format_ = tornadolog.LogFormatter(
        '[%(color)s%(levelname)s%(end_color)s %(asctime)s %(module)s:%(lineno)d]: %(message)s',
    )
    if config.data.logging.path:
        channel = logging.handlers.RotatingFileHandler(
            filename=os.path.join(config.data.logging.path, filename),
            maxBytes=config.data.logging.max_size,
            backupCount=config.data.logging.num_backups,
        )
        channel.setFormatter(format_)
        glogger.addHandler(channel)
    else:# send to console instead of file
        channel = logging.StreamHandler()
        channel.setFormatter(format_)
        glogger.addHandler(channel)
    if to_sentry and config.data.sentry_dsn:
        sentry_sdk.init(
            dsn=config.data.sentry_dsn,
        )