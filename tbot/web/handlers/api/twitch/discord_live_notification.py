import good
from tbot import config, utils
from ..base import Api_handler, Level

class Handler(Api_handler):

    __schema__ = good.Schema({
        'message': good.All(str, good.Length(min=1, max=500)),
        'webhook_url': good.Any(good.Url('https'), good.All(str, good.Length(max=0))),
    })

    @Level(3)
    async def get(self, channel_id):
        r = await self.db.fetchone(
            'SELECT webhook_url, message FROM twitch_discord_live_notification WHERE channel_id=%s',
            (channel_id,)
        )
        if not r:
            self.set_status(204)
        else:
            self.write_object({
                'webhook_url': r['webhook_url'],
                'message': r['message'],
            })

    @Level(3)
    async def put(self, channel_id):
        data = self.validate()
        r = await self.db.fetchone(
            'SELECT webhook_url, message FROM twitch_discord_live_notification WHERE channel_id=%s',
            (channel_id,)
        )
        if not r:
            await self.db.execute('''
                INSERT INTO twitch_discord_live_notification
                    (channel_id, webhook_url, message)
                VALUES 
                    (%s, %s, %s);
            ''', (
                channel_id, 
                data['webhook_url'], 
                data['message'],
            ))
        else:            
            await self.db.execute('''
                UPDATE twitch_discord_live_notification SET
                    webhook_url=%s, message=%s
                WHERE channel_id=%s
            ''', (
                data['webhook_url'], 
                data['message'],
                channel_id, 
            ))