from pathlib import Path

import click
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
    import logging

    from alembic import command
    from alembic.config import Config
    logging.error(Path(__file__).parent / 'alembic.ini')
    cfg = Config(Path(__file__).parent / 'alembic.ini')
    cfg.set_main_option('script_location', 'tbot2:migrations')
    cfg.set_main_option(
        'sqlalchemy.url',
        f'mariadb+pymysql://{config.mysql.user}:{config.mysql.password}@{config.mysql.host}:{config.mysql.port}/{config.mysql.database}',
    )
    command.upgrade(cfg, revision)


def main():
    cli()


if __name__ == '__main__':
    main()
