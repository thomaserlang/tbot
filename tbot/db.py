import logging, aiomysql, pymysql
from . import config

class Db():

    async def connect(self, loop):
        self.pool = await aiomysql.create_pool(
            host=config['mysql']['host'], 
            port=config['mysql']['port'],
            user=config['mysql']['user'], 
            password=config['mysql']['password'],
            db=config['mysql']['database'],
            pool_recycle=3599,
            loop=loop,
            charset='utf8mb4',
            use_unicode=True,
            echo=False,
        )
        return self

    async def fetchone(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.execute(*args, **kwargs)
                r = await c.fetchone()
                return r 
            except pymysql.err.InternalError as e:
                logging.exception('fetchone')
                await c.connection.ping()        
                await c.execute(*args, **kwargs)
                r = await c.fetchone()
                return r 

    async def fetchall(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.execute(*args, **kwargs)
                r = await c.fetchall()
                return r
            except pymysql.err.InternalError as e:
                logging.exception('fetchall')
                await c.connection.ping()            
                await c.execute(*args, **kwargs)
                r = await c.fetchall()

    async def execute(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            await c.execute(*args, **kwargs)
            await c.connection.commit()

class cursor():

    def __init__(self, pool):
        self.pool = pool

    async def __aenter__(self):
        self.conn = await self.pool.acquire()
        self.cur = await self.conn.cursor(aiomysql.DictCursor)
        return self.cur

    async def __aexit__(self, exec_type, exc, tb):
        await self.cur.close()
        self.pool.release(self.conn)
