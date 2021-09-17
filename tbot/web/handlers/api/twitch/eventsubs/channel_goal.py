import logging
from . import eventsub

class Begin_handler(eventsub.Handler):

    async def notification(self):
        logging.info(self.request.body)


class Progress_handler(eventsub.Handler):

    async def notification(self):
        logging.info(self.request.body)
        

class End_handler(eventsub.Handler):

    async def notification(self):
        logging.info(self.request.body)