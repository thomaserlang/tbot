from tbot import logger
from . import eventsub


class Handler(eventsub.Handler):

    async def notification(self):
        logger.info(self.request.body)