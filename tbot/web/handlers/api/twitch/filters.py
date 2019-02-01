import logging, good, copy, asyncio
from ..base import Api_handler, Level, Api_exception
from tbot import config, utils

class Filters(Api_handler):

    @Level(1)
    async def get(self, channel_id):
        filters = await self.db.fetchall(
            'SELECT * FROM twitch_filters WHERE channel_id=%s',
            (channel_id,)
        )
        fs = {}
        for f in filters:
            f['enabled'] = f['enabled'] == 'Y'
            f['warning_enabled'] = f['warning_enabled'] == 'Y'
            fs[f['type']] = f
        self.write_object(fs)

__base_schema__ = good.Schema({
    'enabled': good.Boolean(),
    'exclude_user_level': good.Coerce(int),
    'warning_enabled': good.Boolean(),
    'warning_message': good.All(str, good.Length(min=0, max=200)),
    'warning_expire': good.Coerce(int),
    'timeout_message': good.All(str, good.Length(min=0, max=200)),
    'timeout_duration': good.Coerce(int),
})

async def get_filter(self, channel_id, type_):
    f = await self.db.fetchone(
        'SELECT * FROM twitch_filters WHERE channel_id=%s and type=%s',
        (channel_id, type_,)
    )
    if not f:
        return
    f['enabled'] = f['enabled'] == 'Y'
    f['warning_enabled'] = f['warning_enabled'] == 'Y'
    return f

async def save_filter(self, channel_id, type_, data):
    if not data: 
        return
    fields = ','.join([f for f in data])
    values = ','.join(['%s' for f in data])
    dup = ','.join(['{0}=VALUES({0})'.format(f) for f in data])

    if 'enabled' in data:
        data['enabled'] = 'Y' if data['enabled'] else 'N'
    if 'warning_enabled' in data:
        data['warning_enabled'] = 'Y' if data['warning_enabled'] else 'N'

    await self.db.execute('''
        INSERT INTO twitch_filters 
            (channel_id, type, {})
        VALUES
            (%s, %s, {})
        ON DUPLICATE KEY UPDATE 
            {}
    '''.format(fields, values, dup), 
        (channel_id, type_, *data.values())
    )

class Filter_link(Api_handler):
    
    __schema__ = good.Schema({
        'whitelist': [str],
    }, extra_keys=good.Remove)

    async def get(self, channel_id):
        whitelist = self.db.fetchone(
            'SELECT whitelist FROM twitch_filter_link WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'link'),
            whitelist, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        f['whitelist'] = utils.json_loads(r[1]['whitelist']) \
            if r[1] and r[1]['whitelist'] \
                else []
        self.write_object(f)

    async def put(self, channel_id):
        extra = {
            'whitelist': self.request.body.pop('whitelist'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'link', data),
            self.db.execute('''
                INSERT INTO twitch_filter_link 
                    (channel_id, whitelist) 
                VALUES 
                    (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                    whitelist=VALUES(whitelist)
                ''',
                (channel_id, utils.json_dumps(extra['whitelist']),)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_link', channel_id]
        )
        self.set_status(204)