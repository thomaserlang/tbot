from ..base import Api_handler

class Handler(Api_handler):

    async def get(self, channel_id):
        suggest_name = self.get_argument('suggest_name')
        users = await self.db.fetchall(
            'SELECT user_id as id, user as name FROM logitch.usernames WHERE user like %s LIMIT 5', 
            [suggest_name + '%'])
        self.write_object(users)