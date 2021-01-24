import logging, good
from datetime import datetime
from ..base import Api_handler, Level
from tbot import utils

def validate_cmd():
    def f(v):
        try:
            utils.validate_cmd(v)
            return v
        except Exception as e:
            raise good.Invalid(str(e))
    return f

def validate_response():
    def f(v):
        try:
            utils.validate_cmd_response(v)
            return v
        except Exception as e:
            raise good.Invalid(str(e))
    return f

_schema = {
    'cmd': good.All(str, validate_cmd()),
    'response': good.All(str, validate_response()),
    good.Optional('user_level'): good.All(good.Coerce(int), good.Range(min=0, max=9)),
    good.Optional('enabled_status'): good.All(good.Coerce(int), good.Range(min=0, max=2)),
    good.Optional('global_cooldown'): good.All(good.Coerce(int), good.Range(min=0, max=86400)),
    good.Optional('user_cooldown'): good.All(good.Coerce(int), good.Range(min=0, max=86400)),
    good.Optional('mod_cooldown'): good.All(good.Coerce(int), good.Range(min=0, max=86400)),
    good.Optional('enabled'): good.All(good.Coerce(int), good.Range(min=0, max=1)),
    good.Optional('public'): good.All(good.Coerce(int), good.Range(min=0, max=1)),
    good.Optional('group_name'): good.Maybe(good.All(str, good.Length(min=0, max=50))),
}

class Collection_handler(Api_handler):

    __schema__ = good.Schema(_schema, default_keys=good.Required)

    @Level(1)
    async def get(self, channel_id):
        cmds = await self.db.fetchall('''
            SELECT *
            FROM twitch_commands
            WHERE channel_id=%s
            ORDER BY updated_at DESC
        ''', (channel_id,))
        self.write_object(cmds)

    @Level(1)
    async def post(self, channel_id):
        data = self.validate()
        data['channel_id'] = channel_id
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        fields = ','.join([f for f in data])
        vfields = ','.join(['%s' for f in data])
        values = list(data.values())
        c = await self.db.execute(
            'INSERT INTO twitch_commands ({}) VALUES ({})'.format(fields, vfields),
            values
        )
        cmd = await get_command(self, channel_id, c.lastrowid)
        self.set_status(201)
        self.write_object(cmd)

class Handler(Api_handler):

    __schema__ = good.Schema(_schema, default_keys=good.Optional)

    @Level(1)
    async def get(self, channel_id, id_):
        cmd = await get_command(self, channel_id, id_)
        if not cmd:
            self.set_status(404)
            self.write_object({'error': 'Unknown command'})
        else:
            self.write_object(cmd)

    @Level(1)
    async def put(self, channel_id, id_):
        data = self.validate()
        data['updated_at'] = datetime.utcnow()
        fields = ','.join(['{}=%s'.format(k) for k in data])
        values = list(data.values())
        values.append(channel_id)
        values.append(id_)
        await self.db.execute(
            'UPDATE twitch_commands SET {} WHERE channel_id=%s AND id=%s'.format(fields),
            values
        )
        cmd = await get_command(self, channel_id, id_)
        self.write_object(cmd)

    @Level(1)
    async def delete(self, channel_id, id_):
        cmd = await self.db.execute('''
            DELETE FROM twitch_commands WHERE channel_id=%s and id=%s
        ''', (channel_id, id_,))
        self.set_status(204)

async def get_command(self, channel_id, id_):
    cmd = await self.db.fetchone('''
        SELECT *
        FROM twitch_commands
        WHERE channel_id=%s and id=%s
    ''', (channel_id, id_,))
    return cmd

class Public_collection(Api_handler):

    async def get(self, channel_id):
        cmds = await self.db.fetchall('''
            SELECT *
            FROM twitch_commands
            WHERE channel_id=%s AND public=1
            ORDER BY user_level, group_name, cmd
        ''', (channel_id,))
        self.write_object(cmds)

class Template_collection(Api_handler):

    async def get(self):
        cmds = await self.db.fetchall('''
            SELECT * 
            FROM twitch_commands 
            WHERE channel_id=0 
            ORDER BY group_name, title
        ''')
        self.write_object(cmds)