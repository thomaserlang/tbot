import logging
from ..base import Api_handler, Level, Api_exception
from tbot import config, utils

class Handler(Api_handler):

    @Level(4)
    async def get(self, channel_id):
        channel = await self.db.fetchone(
            'SELECT twitch_token, twitch_scope FROM twitch_channels WHERE channel_id=%s',
            (channel_id,)   
        )
        if not channel:
            raise Api_exception(404, 'Unknown channel')
        scope = []
        if channel['twitch_scope']:
            scope = utils.json_loads(channel['twitch_scope'])
        has_extra_auth = set(scope) == \
            set(config['twitch']['request_scope'])
        if not channel['twitch_token']:
            has_extra_auth = False
        self.write_object({
            'has_extra_auth': has_extra_auth,
        })