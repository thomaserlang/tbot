import logging, good
from tornado import web
from ..base import Api_handler, Level

class Handler(Api_handler):

    __schema__ = good.Schema({
        str: [{
            'message': good.All(str, good.Length(min=0, max=200)),
            good.Optional('min_amount'): good.All(good.Coerce(int), good.Range(min=0, max=1000)),
        }],
    }, default_keys=good.Optional)

    @Level(1)
    async def get(self, channel_id):
        alerts = await self.db.fetchall(
            'SELECT type, message, min_amount FROM twitch_chat_alerts WHERE channel_id=%s',
            (channel_id,)
        )
        grouped_alerts = {}
        for a in alerts:
            l = grouped_alerts.setdefault(a['type'], [])
            l.append({
                'message': a['message'],
                'min_amount': a['min_amount'] or 0,
            })
        self.write_object(grouped_alerts)

    @Level(1)
    async def put(self, channel_id):
        data = self.validate()
        for key in data:
            ins = []
            for d in data[key]:
                if d['message']:
                    ins.append((
                        channel_id,
                        key,
                        d['message'], 
                        d.get('min_amount', 0),
                    ))
            await self.db.execute(
                'DELETE FROM twitch_chat_alerts WHERE channel_id=%s AND type=%s;', 
                (channel_id, key,)
            )
            if ins:
                await self.db.executemany('''
                    INSERT INTO twitch_chat_alerts 
                        (channel_id, type, message, min_amount)
                    VALUES 
                        (%s, %s, %s, %s)
                    ''', ins
                )
        await self.get(channel_id)