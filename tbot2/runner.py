import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import click
import uvicorn
from loguru import logger

from tbot2.config_settings import config


@click.group()
def cli() -> None: ...


@cli.command()
def api() -> None:
    uvicorn.run(
        'tbot2.main:app',
        host='0.0.0.0',
        port=config.port,
        reload=config.debug,
        proxy_headers=True,
        forwarded_allow_ips='*',
        log_level=config.logging.level,
    )


@cli.command()
@click.option('--revision', '-r', help='revision, default head', default='head')
@click.option('--keep-running', is_flag=True, help='Keep the process running forever')
def upgrade(revision: str, keep_running: bool) -> None:
    from alembic import command
    from alembic.config import Config

    cfg = Config(Path(__file__).parent / 'alembic.ini')
    cfg.set_main_option('script_location', 'tbot2:migrations')
    cfg.set_main_option(
        'sqlalchemy.url',
        f'mariadb+pymysql://{config.db.user}:{config.db.password}@{config.db.host}:{config.db.port}/{config.db.database}',
    )
    command.upgrade(cfg, revision)

    if keep_running:
        logger.info('Running forever...')

        async def run_forever() -> None:
            while True:
                await asyncio.sleep(3600)

        with asyncio.Runner() as runner:
            runner.run(run_forever())


@asynccontextmanager
async def db() -> AsyncGenerator[None]:
    from tbot2.database import database

    await database.setup()
    yield
    await database.close()


@cli.command()
def refresh_twitch_eventsubs() -> None:
    from tbot2.twitch import refresh_all_eventsubs

    async def run() -> None:
        async with db():
            await refresh_all_eventsubs()

    with asyncio.Runner() as runner:
        runner.run(run())


@cli.command()
def tasks() -> None:
    from tbot2.channel_timer import task_handle_timers
    from tbot2.twitch import task_update_live_streams
    from tbot2.youtube import task_youtube_live

    async def run() -> None:
        async with db():
            await asyncio.gather(
                task_update_live_streams(),
                task_handle_timers(),
                task_youtube_live(),
            )

    with asyncio.Runner() as runner:
        runner.run(run())


def main() -> None:
    cli()


if __name__ == '__main__':
    main()
