import logging, good, asyncio
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
        'whitelist': good.All(
            [good.All(str, good.Length(min=1, max=50))], good.Length(min=0, max=100)),
    })

    @Level(1)
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

    @Level(1)
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


class Filter_paragraph(Api_handler):
    
    __schema__ = good.Schema({
        'max_length': good.Coerce(int),
    })

    @Level(1)
    async def get(self, channel_id):
        paragraph = self.db.fetchone(
            'SELECT max_length FROM twitch_filter_paragraph WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'paragraph'),
            paragraph, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        self.write_object({**f, **r[1]})

    @Level(1)
    async def put(self, channel_id):
        extra = {
            'max_length': self.request.body.pop('max_length'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'paragraph', data),
            self.db.execute('''
                INSERT INTO twitch_filter_paragraph
                    (channel_id, max_length) 
                VALUES 
                    (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                    max_length=VALUES(max_length)
                ''',
                (channel_id, extra['max_length'],)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_paragraph', channel_id]
        )
        self.set_status(204)

class Filter_symbol(Api_handler):
    
    __schema__ = good.Schema({
        'max_symbols': good.Coerce(int),
    })

    @Level(1)
    async def get(self, channel_id):
        symbol = self.db.fetchone(
            'SELECT max_symbols FROM twitch_filter_symbol WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'symbol'),
            symbol, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        self.write_object({**f, **r[1]})

    @Level(1)
    async def put(self, channel_id):
        extra = {
            'max_symbols': self.request.body.pop('max_symbols'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'symbol', data),
            self.db.execute('''
                INSERT INTO twitch_filter_symbol
                    (channel_id, max_symbols) 
                VALUES 
                    (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                    max_symbols=VALUES(max_symbols)
                ''',
                (channel_id, extra['max_symbols'],)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_symbol', channel_id]
        )
        self.set_status(204)

class Filter_caps(Api_handler):
    
    __schema__ = good.Schema({
        'min_length': good.Coerce(int),
        'max_percent': good.Coerce(int),
    })

    @Level(1)
    async def get(self, channel_id):
        caps = self.db.fetchone(
            'SELECT min_length, max_percent FROM twitch_filter_caps WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'caps'),
            caps, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        self.write_object({**f, **r[1]})

    @Level(1)
    async def put(self, channel_id):
        extra = {
            'min_length': self.request.body.pop('min_length'),
            'max_percent': self.request.body.pop('max_percent'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'caps', data),
            self.db.execute('''
                INSERT INTO twitch_filter_caps
                    (channel_id, min_length, max_percent) 
                VALUES 
                    (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE 
                    min_length=VALUES(min_length),
                    max_percent=VALUES(max_percent)
                ''',
                (channel_id, extra['min_length'], extra['max_percent'],)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_caps', channel_id]
        )
        self.set_status(204)

class Filter_emote(Api_handler):
    
    __schema__ = good.Schema({
        'max_emotes': good.Coerce(int),
    })

    @Level(1)
    async def get(self, channel_id):
        emote = self.db.fetchone(
            'SELECT max_emotes FROM twitch_filter_emote WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'emote'),
            emote, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        self.write_object({**f, **r[1]})

    @Level(1)
    async def put(self, channel_id):
        extra = {
            'max_emotes': self.request.body.pop('max_emotes'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'emote', data),
            self.db.execute('''
                INSERT INTO twitch_filter_emote
                    (channel_id, max_emotes) 
                VALUES 
                    (%s, %s) 
                ON DUPLICATE KEY UPDATE 
                    max_emotes=VALUES(max_emotes)
                ''',
                (channel_id, extra['max_emotes'],)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_emote', channel_id]
        )
        self.set_status(204)

class Filter_non_latin(Api_handler):
    
    __schema__ = good.Schema({
        'min_length': good.Coerce(int),
        'max_percent': good.Coerce(int),
    })

    @Level(1)
    async def get(self, channel_id):
        non_latin = self.db.fetchone(
            'SELECT min_length, max_percent FROM twitch_filter_non_latin WHERE channel_id=%s',
            (channel_id,)
        )
        r = await asyncio.gather(
            get_filter(self, channel_id, 'non-latin'),
            non_latin, 
        )
        f = r[0]
        if not f:
            self.set_status(204)
            return
        self.write_object({**f, **r[1]})

    @Level(1)
    async def put(self, channel_id):
        extra = {
            'min_length': self.request.body.pop('min_length'),
            'max_percent': self.request.body.pop('max_percent'),
        }
        data = self.validate(__base_schema__)
        extra = self._validate(extra, self.__schema__)
        await asyncio.gather(
            save_filter(self, channel_id, 'non-latin', data),
            self.db.execute('''
                INSERT INTO twitch_filter_non_latin
                    (channel_id, min_length, max_percent) 
                VALUES 
                    (%s, %s, %s) 
                ON DUPLICATE KEY UPDATE 
                    min_length=VALUES(min_length),
                    max_percent=VALUES(max_percent)
                ''',
                (channel_id, extra['min_length'], extra['max_percent'],)
            )
        )        
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_non_latin', channel_id]
        )
        self.set_status(204)


class Filter_action(Api_handler):
    
    @Level(1)
    async def get(self, channel_id):
        f = await get_filter(self, channel_id, 'action')
        if not f:
            self.set_status(204)
            return
        self.write_object(f)

    @Level(1)
    async def put(self, channel_id):
        data = self.validate(__base_schema__)
        await save_filter(self, channel_id, 'action', data)   
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_action', channel_id]
        )
        self.set_status(204)