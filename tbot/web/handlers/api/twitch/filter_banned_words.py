import logging, good, asyncio
from ..base import Api_handler, Level, Api_exception
from . import filters
from tbot import config, utils, twitch_bot
from tbot.twitch_bot.filters.banned_words import check_message

class Group_handler(filters.Filter_base):
    
    @Level(1)
    async def get(self, channel_id, filter_id):
        f = await self.get_filter(channel_id, 'banned_words', filter_id)
        if not f:
            self.set_status(204)
            return
        banned_words = await self.db.fetchall('''
            SELECT id, banned_words 
            FROM twitch_filter_banned_words
            WHERE channel_id=%s AND filter_id=%s
        ''', (channel_id, filter_id,))
        f['banned_words'] = banned_words
        self.write_object(f)

    @Level(1)
    async def put(self, channel_id, filter_id):
        extra = {
            'banned_words': self.request.body.pop('banned_words', []),
        }
        data = self.validate()
        data['id'] = filter_id
        await self.save_filter(channel_id, 'banned_words', False, data)
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_banned_words', channel_id, filter_id]
        )
        self.set_status(204)

    @Level(1)
    async def delete(self, channel_id, filter_id):
        f = await self.db.execute(
            'DELETE FROM twitch_filters WHERE channel_id=%s and type="banned_words" and id=%s',
            (channel_id, filter_id,)
        )        
        self.set_status(204)

    async def save_banned_words(self, channel_id, filter_id, banned_words, delete_banned_words=[]):
        for bw in banned_words:
            if not bw['id'] or bw['id'] < 1:
                await self.db.execute('''
                    INSERT INTO twitch_filter_banned_words (channel_id, filter_id, banned_words)
                    VALUES (%s, %s, %s)
                ''', (channel_id, filter_id, bw['banned_words']))
            else:
                await self.db.execute('''
                    UPDATE twitch_filter_banned_words SET banned_words=%s 
                    WHERE id=%s and channel_id=%s and filter_id=%s
                ''', (bw['banned_words'], bw['id'], channel_id, filter_id,))
        for bw in delete_banned_words:
            await self.db.execute('''
                DELETE FROM twitch_filter_banned_words 
                WHERE id=%s and channel_id=%s and filter_id=%s
            ''', (bw['id'], channel_id, filter_id,))

class Groups_handler(Group_handler):

    @Level(1)
    async def get(self, channel_id):
        f = await self.get_filters(channel_id, 'banned_words')
        self.write_object(f)

    @Level(1)
    async def post(self, channel_id):
        extra = {
            'banned_words': self.request.body.pop('banned_words', []),
        }
        data = self.validate()
        filter_id = await self.save_filter(channel_id, 'banned_words', False, data)
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_banned_words', channel_id, filter_id]
        )
        await super().get(channel_id, filter_id)

class Banned_words_handler(Api_handler):

    __schema__ = good.Schema({
        'banned_words': good.All(str, good.Length(min=1, max=1000)),
    })

    @Level(1)
    async def post(self, channel_id, filter_id):
        d = self.validate()
        c = await self.db.execute('''
            INSERT INTO twitch_filter_banned_words 
            (channel_id, filter_id, banned_words)
            VALUES
            (%s, %s, %s)
        ''', (channel_id, filter_id, d['banned_words']))
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_banned_words', channel_id, filter_id]
        )
        self.set_status(201)
        self.write_object({
            'id': c.lastrowid,
            'banned_words': d['banned_words'],
        })

    @Level(1)
    async def put(self, channel_id, filter_id, id_):
        d = self.validate()
        await self.db.execute('''
            UPDATE twitch_filter_banned_words SET banned_words=%s 
            WHERE id=%s and channel_id=%s and filter_id=%s
        ''', (d['banned_words'], id_, channel_id, filter_id,))
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_banned_words', channel_id, filter_id]
        )
        self.set_status(204)

    @Level(1)
    async def delete(self, channel_id, filter_id, id_):
        await self.db.execute('''
            DELETE FROM twitch_filter_banned_words 
            WHERE id=%s and channel_id=%s and filter_id=%s
        ''', (id_, channel_id, filter_id,))
        r = await self.redis.publish_json(
            'tbot:server:commands', 
            ['reload_filter_banned_words', channel_id, filter_id]
        )
        self.set_status(204)

class Banned_words_test_handler(Api_handler):

    __schema__ = good.Schema({
        'message': str,
    })

    @Level(1)
    async def post(self, channel_id, filter_id):
        d = self.validate()
        banned_words = await self.db.fetchall('''
            SELECT banned_words 
            FROM twitch_filter_banned_words
            WHERE channel_id=%s AND filter_id=%s
        ''', (channel_id, filter_id,))
        self.write_object({
            'match': check_message(d['message'], [bw['banned_words'] for bw in banned_words])
        })