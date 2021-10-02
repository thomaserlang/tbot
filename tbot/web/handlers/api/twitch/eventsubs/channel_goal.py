import logging
from . import eventsub

class Handler(eventsub.Handler):

    async def notification(self):
        bid = self.request.body['event']['broadcaster_user_id']
        typ = self.request.body['event']['type']
        self.request.body['event']['sub_type'] = self.request.body['subscription']['type']
        r = await self.redis.publish_json(
            f'twitch:widget:goal:{bid}:{typ}', 
            self.request.body['event']
        )