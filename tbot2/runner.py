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


def main():
    cli()


if __name__ == '__main__':
    main()
