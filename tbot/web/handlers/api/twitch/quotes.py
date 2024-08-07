import good
from datetime import datetime, time
from ..base import Api_handler, Level

_schema = {
    'message': good.All(str, good.Length(min=1, max=400)),
    'date': good.Date('%Y-%m-%d'),
}

class Collection_handler(Api_handler):

    __schema__ = good.Schema(_schema, default_keys=good.Required)

    @Level(1)
    async def get(self, channel_id):
        cmds = await self.db.fetchall('''
            SELECT *
            FROM twitch_quotes
            WHERE channel_id=%s AND enabled=1
            ORDER BY number DESC
        ''', (channel_id,))
        self.write_object(cmds)

    @Level(1)
    async def post(self, channel_id):
        data = self.validate()
        data['channel_id'] = channel_id
        data['created_at'] = datetime.combine(data['date'], time(0, 0, 0))
        data['updated_at'] = datetime.utcnow()
        raise Exception('Not implemented')
        # TODO: get user name
        #date['created_by'] = self.current_user.
        fields = ','.join([f for f in data])
        vfields = ','.join(['%s' for _ in data])
        values = list(data.values())
        c = await self.db.execute(
            'INSERT INTO twitch_quotes ({}) VALUES ({})'.format(fields, vfields),
            values
        )
        cmd = await get_quote(self, channel_id, c.lastrowid)
        self.set_status(201)
        self.write_object(cmd)

class Handler(Api_handler):

    __schema__ = good.Schema(_schema, default_keys=good.Optional)

    @Level(1)
    async def get(self, channel_id, number):
        cmd = await get_quote(self, channel_id, number)
        if not cmd:
            self.set_status(404)
            self.write_object({'error': 'Unknown quote'})
        else:
            self.write_object(cmd)

    @Level(1)
    async def put(self, channel_id, number):
        data = self.validate()
        data['updated_at'] = datetime.utcnow()
        if 'date' in data:
            if data['date']:
                data['created_at'] = datetime.combine(data['date'], time(0, 0, 0))
            del data['date']
        fields = ','.join(['{}=%s'.format(k) for k in data])
        values = list(data.values())
        values.append(channel_id)
        values.append(number)
        await self.db.execute(
            'UPDATE twitch_quotes SET {} WHERE channel_id=%s AND number=%s'.format(fields),
            values
        )
        cmd = await get_quote(self, channel_id, number)
        self.write_object(cmd)

    @Level(1)
    async def delete(self, channel_id, number):
        await self.db.execute('''
            UPDATE twitch_quotes SET enabled=0 WHERE channel_id=%s and number=%s
        ''', (channel_id, number,))
        self.set_status(204)

async def get_quote(self, channel_id, number):
    cmd = await self.db.fetchone('''
        SELECT *
        FROM twitch_quotes
        WHERE channel_id=%s and number=%s
    ''', (channel_id, number,))
    return cmd