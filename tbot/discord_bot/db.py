import logging, aiomysql
from tbot.discord_bot import bot

class cursor():

    async def __aenter__(self):
        self.conn = await bot.pool.acquire()
        self.cur = await self.conn.cursor(aiomysql.DictCursor)
        return self.cur

    async def __aexit__(self, exec_type, exc, tb):
        await self.cur.close()
        bot.pool.release(self.conn)

async def fetchone(*args, **kwargs):
    async with cursor() as c:
        await c.execute(*args, **kwargs)
        r = await c.fetchone()
        return r 

async def fetchall(*args, **kwargs):
    async with cursor() as c:
        await c.execute(*args, **kwargs)
        r = await c.fetchall()
        return r 

async def execute(*args, **kwargs):
    async with cursor() as c:
        await c.execute(*args, **kwargs)
        await c.connection.commit()