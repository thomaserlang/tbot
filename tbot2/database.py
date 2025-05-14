import os
from warnings import filterwarnings

import redis.asyncio as redis
import sqlalchemy as sa
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from tbot2.config_settings import config

filterwarnings('ignore', module=r'aiomysql')


class Connections:
    def __init__(self) -> None:
        self.engine: AsyncEngine
        self.session: async_sessionmaker[AsyncSession]
        self.redis: redis.Redis
        self._test_setup: bool = False
        self._conn: AsyncConnection
        self.elasticsearch = AsyncElasticsearch(
            config.elasticsearch.host,
            basic_auth=(config.elasticsearch.user, config.elasticsearch.password),
            verify_certs=config.elasticsearch.verify_certs,
        )

    async def setup(self) -> None:
        database_url = sa.URL.create(
            drivername=config.db.drivername,
            username=config.db.user,
            password=config.db.password,
            host=config.db.host,
            port=config.db.port,
            database=config.db.database,
        )

        self.engine = create_async_engine(
            database_url,
            echo=False,
            pool_pre_ping=True,
            pool_size=32,
            max_overflow=64,
        )
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

        self.redis = redis.Redis(
            host=config.redis.host,
            port=config.redis.port,
            password=config.redis.password,
            db=config.redis.db,
            decode_responses=True,
        )

    async def setup_test(self) -> None:
        config.redis.db = 15
        config.db.database = 'tbot-testdb'

        if not self._test_setup:
            u = sa.URL.create(
                drivername='mariadb+pymysql',
                username=config.db.user,
                password=config.db.password,
                host=config.db.host,
                port=config.db.port,
            )
            engine = sa.create_engine(u)
            with engine.begin() as conn:
                conn.execute(
                    sa.text(
                        'CREATE SCHEMA IF NOT EXISTS `tbot-testdb` '
                        'DEFAULT CHARACTER SET utf8mb4;'
                    )
                )
            from alembic import command
            from alembic.config import Config

            u = u.set(database='tbot-testdb')
            cfg = Config(os.path.dirname(os.path.abspath(__file__)) + '/alembic.ini')
            cfg.set_main_option('script_location', 'tbot2:migrations')
            cfg.set_main_option(
                'sqlalchemy.url', u.render_as_string(hide_password=False)
            )
            command.upgrade(cfg, 'head')

        await self.setup()
        self._conn = await self.engine.connect()
        self.session = async_sessionmaker(
            self._conn, expire_on_commit=False, class_=AsyncSession
        )

        self._test_setup = True
        self.trans = await self._conn.begin()

        await self.redis.flushdb()  # type: ignore

    async def close(self) -> None:
        await self.engine.dispose()
        await self.redis.aclose()  # type: ignore
        await self.elasticsearch.close()

    async def close_test(self) -> None:
        await self.trans.rollback()
        await self._conn.close()
        await self.close()


conn = Connections()
