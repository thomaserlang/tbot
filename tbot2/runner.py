from contextlib import asynccontextmanager
from pathlib import Path

import asyncclick as click
import uvicorn

from tbot2.config_settings import config


@click.group()
def cli():
    pass


@cli.command()
def api():
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
def upgrade(revision: str):
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
async def db():
    from tbot2.database import database

    await database.setup()
    yield
    await database.close()


@cli.command()
async def twitch_eventsub_unregister_all():
    from tbot2.twitch import unregister_all_eventsubs

    async with db():
        await unregister_all_eventsubs()


@cli.command()
async def twitch_eventsub_register_all():
    from tbot2.twitch import register_all_eventsubs

    async with db():
        await register_all_eventsubs()


def main():
    cli()


if __name__ == '__main__':
    main()
