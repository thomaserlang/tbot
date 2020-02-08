import logging, good, asyncio
from ..base import Api_handler, Level, Api_exception
from tbot import config, utils
from datetime import datetime, timedelta

__schema__ = {
    'name': good.All(str, good.Length(min=1, max=100)),
    'messages': good.All([good.All(str, good.Length(min=1, max=500))], good.Length(min=1, max=100)),
    good.Optional('enabled'): good.All(good.Coerce(int), good.Range(min=0, max=1)),
    good.Optional('enabled_status'): good.All(good.Coerce(int), good.Range(min=0, max=2)),
    good.Optional('interval'): good.All(good.Coerce(int), good.Range(min=1, max=10080)),
    good.Optional('send_message_order'): good.All(good.Coerce(int), good.Range(min=1, max=2)),
}

class Handler(Api_handler):

    __schema__ = good.Schema(__schema__, default_keys=good.Optional)

    @Level(1)
    async def put(self, channel_id, id_):
        data = self.validate()
        data['updated_at'] = datetime.utcnow()
        if 'interval' in data:
            data['next_run'] = datetime.utcnow()+timedelta(minutes=data['interval'])
        if 'messages' in data:
            data['messages'] = utils.json_dumps(data['messages'])
        fields = ', '.join(['`{}`=%s'.format(k) for k in data])
        values = list(data.values())
        values.append(channel_id)
        values.append(id_)
        await self.db.execute(
            'UPDATE twitch_timers SET {} WHERE channel_id=%s AND id=%s'.format(fields),
            values
        )
        t = await get_timer(self, channel_id, id_)
        self.write_object(t)

    @Level(1)
    async def get(self, channel_id, id_):
        t = await get_timer(self, channel_id, id_)
        if not t:
            raise Api_exception(404, 'Unknown timer')
        self.write_object(t)

    @Level(1)
    async def delete(self, channel_id, id_):
        t = await self.db.execute(
            'DELETE FROM twitch_timers WHERE channel_id=%s AND id=%s',
            (channel_id, id_,)
        )
        self.set_status(204)

class Collection_handler(Api_handler):

    __schema__ = good.Schema(__schema__)

    @Level(1)
    async def post(self, channel_id):
        data = self.validate()
        data['channel_id'] = channel_id
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        data['next_run'] = datetime.utcnow()+timedelta(minutes=data.get('interval', 5))
        if 'messages' in data:
            data['messages'] = utils.json_dumps(data['messages'])
        fields = ','.join(['`'+f+'`' for f in data])
        values = ','.join(['%s' for f in data])
        interval = data.get('interval', 5)
        r = await self.db.execute(
            'INSERT INTO twitch_timers ({}) VALUES ({})'.format(fields, values), 
            list(data.values())
        )
        t = await get_timer(self, channel_id, r.lastrowid)
        if not t:
            raise Api_exception(400, 'Unknown timer')
        self.set_status(201)
        self.write_object(t)

    @Level(1)
    async def get(self, channel_id):
        timers = await self.db.fetchall(
            'SELECT * FROM twitch_timers WHERE channel_id=%s',
            (channel_id,)
        )
        for t in timers:
            t.pop('messages')
        self.write_object(timers)

async def get_timer(self, channel_id, id_):
    t = await self.db.fetchone(
        'SELECT * FROM twitch_timers WHERE id=%s AND channel_id=%s',
        (id_, channel_id)
    )
    if t:
        t['messages'] = utils.json_loads(t['messages']) if t['messages'] else []
    return t