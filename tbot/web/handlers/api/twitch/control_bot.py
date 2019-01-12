from ..base import Api_handler, Level

class Settings_handler(Api_handler):

    @Level(3)
    async def get(self, channel_id):
        r = await self.db.fetchone(
            'SELECT active, muted, chatlog_enabled FROM twitch_channels WHERE channel_id=%s',
            (channel_id)
        )
        if r:
            self.write_object({
                'active': r['active'] == 'Y',
                'muted': r['muted'] == 'Y',
                'chatlog_enabled': r['chatlog_enabled'] == 'Y',
            })
        else:
            self.set_status(204)

class Join_handler(Api_handler):

    @Level(3)
    async def post(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set active="Y" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['join', channel_id]
        )
        self.set_status(204)

    @Level(3)
    async def delete(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set active="N" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['part', channel_id]
        )
        self.set_status(204)

class Mute_handler(Api_handler):

    @Level(3)
    async def post(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set muted="Y" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['mute', channel_id]
        )
        self.set_status(204)

    @Level(3)
    async def delete(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set muted="N" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['unmute', channel_id]
        )
        self.set_status(204)


class Enable_chatlog_handler(Api_handler):

    @Level(3)
    async def post(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set chatlog_enabled="Y" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['enable_chatlog', channel_id]
        )
        self.set_status(204)

    @Level(3)
    async def delete(self, channel_id):
        await self.db.execute(
            'UPDATE twitch_channels set chatlog_enabled="N" where channel_id=%s',
            (channel_id)
        )
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['disable_chatlog', channel_id]
        )
        self.set_status(204)