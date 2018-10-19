from ..base import Api_handler
from tornado import web

class Handler(Api_handler):

    async def get(self):
        sql = 'SELECT channel_id as id, name FROM channels WHERE active="Y"'
        args = []
        name = self.get_argument('name', None)
        suggest_name = self.get_argument('suggest_name', None)
        if name:
            sql += ' AND name=%s'
            args.append(name)
        elif suggest_name:
            sql += ' AND name LIKE %s'
            args.append(suggest_name+'%')
        channels = await self.db.fetchall(sql, args)
        self.write_object(channels)