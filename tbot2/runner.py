import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import asyncclick as click
import uvicorn

from tbot2.config_settings import config


@click.group()
def cli() -> None:
    pass


@cli.command()
def api() -> None:
    uvicorn.run(
        'tbot2.main:app',
        host='0.0.0.0',
        port=config.web.port,
        reload=config.debug,
        proxy_headers=True,
        forwarded_allow_ips='*',
        log_level=config.logging.level,
    )


@cli.command()
@click.option('--revision', '-r', help='revision, default head', default='head')
def upgrade(revision: str) -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(Path(__file__).parent / 'alembic.ini')
    cfg.set_main_option('script_location', 'tbot2:migrations')
    cfg.set_main_option(
        'sqlalchemy.url',
        f'mariadb+pymysql://{config.mysql.user}:{config.mysql.password}@{config.mysql.host}:{config.mysql.port}/{config.mysql.database}',
    )
    command.upgrade(cfg, revision)


@asynccontextmanager
async def db() -> AsyncGenerator[None]:
    from tbot2.database import database

    await database.setup()
    yield
    await database.close()


@cli.command()
async def refresh_twitch_eventsubs() -> None:
    from tbot2.twitch import refresh_all_eventsubs

    async with db():
        await refresh_all_eventsubs()


@cli.command()
async def tasks() -> None:
    from tbot2.twitch import task_update_viewer_streams

    async with db():
        await asyncio.gather(task_update_viewer_streams())


def main() -> None:
    cli()


if __name__ == '__main__':
    main()
