import logging, good, json
from tornado import web
from ..base import Api_handler, Level

class Points_settings_handler(Api_handler):

    __schema__ = good.Schema({
        'enabled': good.Boolean(),
        'points_name': good.All(str, good.Length(min=1, max=45)),
        'points_per_min': good.All(good.Coerce(int), good.Range(min=0)),
        'points_per_min_sub_multiplier': good.All(good.Coerce(int), good.Range(min=0)),
        'points_per_sub': good.All(good.Coerce(int), good.Range(min=0)),
        'points_per_cheer': good.All(good.Coerce(int), good.Range(min=0)),
        'ignore_users': [str],
    })

    async def get(self, channel_id):
        settings = await self.db.fetchone(
            'select * from twitch_channel_point_settings where channel_id=%s',
            (channel_id),
        )
        if not settings:
            self.set_status(204)
        else:
            self.write_object({
                'enabled': True if settings['enabled'] == 1 else False,
                'points_name': settings['points_name'],
                'points_per_min': settings['points_per_min'],
                'points_per_min_sub_multiplier': settings['points_per_min_sub_multiplier'],
                'points_per_sub': settings['points_per_sub'],
                'points_per_cheer': settings['points_per_cheer'],
                'ignore_users': json.loads(settings['ignore_users']),
            })

    @Level(3)
    async def put(self, channel_id):
        data = self.validate()
        if 'ignore_users' in data:
            data['ignore_users'] = json.dumps(data['ignore_users'])
        fields = ','.join([f for f in data])
        values = ','.join(['%s' for f in data])
        dup = ','.join([f'{f}=VALUES({f})' for f in data])

        await self.db.execute(f'''
            INSERT INTO 
                twitch_channel_point_settings
                (channel_id, {fields})
            VALUES
                (%s, {values})
            ON DUPLICATE KEY UPDATE {dup}
        ''', (
            channel_id,
            *data.values(),
        ))
        self.set_status(204)

class Slots_handler(Api_handler):

    __schema__ = good.Schema({
        'emote_pool_size': good.All(good.Coerce(int), good.Range(min=2)),
        'payout_percent': good.All(good.Coerce(int), good.Range(min=1)),
        'min_bet': good.All(good.Coerce(int), good.Range(min=1)),
        'max_bet': good.All(good.Coerce(int), good.Range(min=0)),
        'emotes': [str],
        'win_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'allin_win_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'lose_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'allin_lose_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
    })

    async def get(self, channel_id):
        settings = await self.db.fetchone(
            'select * from twitch_gambling_slots_settings where channel_id=%s',
            (channel_id),
        )
        if not settings:
            self.set_status(204)
        else:
            settings.pop('channel_id')
            settings['emotes'] = json.loads(settings['emotes'])
            self.write_object(settings)

    @Level(3)
    async def put(self, channel_id):
        data = self.validate()
        if 'emotes' in data:
            data['emotes'] = json.dumps(data['emotes'])
        fields = ','.join([f for f in data])
        values = ','.join(['%s' for f in data])
        dup = ','.join([f'{f}=VALUES({f})' for f in data])

        await self.db.execute(f'''
            INSERT INTO 
                twitch_gambling_slots_settings
                (channel_id, {fields})
            VALUES
                (%s, {values})
            ON DUPLICATE KEY UPDATE {dup}
        ''', (
            channel_id,
            *data.values(),
        ))
        self.set_status(204)


class Roulette_handler(Api_handler):

    __schema__ = good.Schema({
        'win_chance': good.All(good.Coerce(int), good.Range(min=0, max=100)),
        'min_bet': good.All(good.Coerce(int), good.Range(min=1)),
        'max_bet': good.All(good.Coerce(int), good.Range(min=0)),
        'win_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'allin_win_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'lose_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
        'allin_lose_message': good.All(good.Coerce(str), good.Length(min=1, max=250)),
    })

    async def get(self, channel_id):
        settings = await self.db.fetchone(
            'select * from twitch_gambling_roulette_settings where channel_id=%s',
            (channel_id),
        )
        if not settings:
            self.set_status(204)
        else:
            settings.pop('channel_id')
            self.write_object(settings)

    @Level(3)
    async def put(self, channel_id):
        data = self.validate()
        if 'emotes' in data:
            data['emotes'] = json.dumps(data['emotes'])
        fields = ','.join([f for f in data])
        values = ','.join(['%s' for f in data])
        dup = ','.join([f'{f}=VALUES({f})' for f in data])

        await self.db.execute(f'''
            INSERT INTO 
                twitch_gambling_roulette_settings
                (channel_id, {fields})
            VALUES
                (%s, {values})
            ON DUPLICATE KEY UPDATE {dup}
        ''', (
            channel_id,
            *data.values(),
        ))
        self.set_status(204)