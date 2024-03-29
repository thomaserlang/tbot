import aiomysql, pymysql
from tbot import config, logger

class Db():

    async def connect(self, loop=None):
        self.pool = await aiomysql.create_pool(
            host=config.data.mysql.host, 
            port=config.data.mysql.port,
            user=config.data.mysql.user, 
            password=config.data.mysql.password,
            db=config.data.mysql.database,
            pool_recycle=3599,
            loop=loop,
            charset='utf8mb4',
            use_unicode=True,
            echo=False,
            autocommit=False,
        )
        return self

    async def fetchone(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.execute(*args, **kwargs)
                r = await c.fetchone()
                await c.connection.commit()
                return r 
            except (pymysql.err.InternalError, pymysql.err.OperationalError):
                logger.exception('fetchone')
                await c.connection.ping()        
                await c.execute(*args, **kwargs)
                r = await c.fetchone()
                await c.connection.commit()
                return r 

    async def fetchall(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.execute(*args, **kwargs)
                r = await c.fetchall()
                await c.connection.commit()
                return r
            except (pymysql.err.InternalError, pymysql.err.OperationalError):
                logger.exception('fetchall')
                await c.connection.ping()            
                await c.execute(*args, **kwargs)
                r = await c.fetchall()
                await c.connection.commit()
                return r

    async def execute(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.execute(*args, **kwargs)
                await c.connection.commit()
                return c
            except (pymysql.err.InternalError, pymysql.err.OperationalError):
                logger.exception('execute')
                await c.connection.ping()
                await c.execute(*args, **kwargs)
                await c.connection.commit()
                return c

    async def executemany(self, *args, **kwargs):
        async with cursor(self.pool) as c:
            try:
                await c.executemany(*args, **kwargs)
                await c.connection.commit()
                return c
            except (pymysql.err.InternalError, pymysql.err.OperationalError):
                logger.exception('executemany')
                await c.connection.ping()
                await c.executemany(*args, **kwargs)
                await c.connection.commit()
                return c

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