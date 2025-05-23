import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path
from uuid import UUID

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
    from tbot2.database import conn

    await conn.setup()
    yield
    await conn.close()


@cli.command()
def twitch_eventsubs_sync() -> None:
    from tbot2.twitch import sync_all_eventsubs

    async def run() -> None:
        async with db():
            await sync_all_eventsubs()

    with asyncio.Runner() as runner:
        runner.run(run())


@cli.command()
def twitch_eventsubs_unregister() -> None:
    from tbot2.twitch import unregister_all_eventsubs

    async def run() -> None:
        async with db():
            await unregister_all_eventsubs()

    with asyncio.Runner() as runner:
        runner.run(run())


@cli.command()
def tasks() -> None:
    from tbot2.channel_timer import timer_tasks
    from tbot2.tiktok import tiktok_tasks
    from tbot2.twitch import twitch_tasks
    from tbot2.youtube import youtube_tasks

    async def run() -> None:
        async with db():
            fns = [
                timer_tasks(),
                twitch_tasks(),
                youtube_tasks(),
                tiktok_tasks(),
            ]
            await asyncio.wait(
                [asyncio.create_task(fn) for fn in fns],
                return_when=asyncio.FIRST_EXCEPTION,
            )

    with asyncio.Runner() as runner:
        runner.run(run())


@cli.command()
@click.option('--channel-id', help='Channel ID', required=True)
def seed_data(channel_id: str) -> None:
    from tbot2.channel_activity import seed_activity
    from tbot2.channel_chat_message import seed_chat_messages

    async def run() -> None:
        async with db():
            await asyncio.gather(
                seed_activity(channel_id=UUID(channel_id)),
                seed_chat_messages(channel_id=UUID(channel_id), num_messages=250),
            )

    with asyncio.Runner() as runner:
        runner.run(run())


def main() -> None:
    cli()


if __name__ == '__main__':
    main()
