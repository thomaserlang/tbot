import click
import asyncio
from tbot import config, config_load, logger

@click.group()
@click.option('--config', default=None, help='path to the config file')
@click.option('--log_path', '-lp', default=None, help='a folder to store the log files in')
@click.option('--log_level', '-ll', default=None, help='notset, debug, info, warning, error or critical')
def cli(config, log_path, log_level):
    config_load(config)
    if log_path != None:
        config['logging']['path'] = log_path
    if log_level:
        config['logging']['level'] = log_level

@click.command()
def twitch_irc():
    logger.set_logger('twitch_irc.log')

    loop = asyncio.get_event_loop()

    import tbot.irc
    loop.create_task(tbot.irc.main().connect())

    loop.run_forever()

@cli.command()
def web():
    logger.set_logger('web.log')
    import tbot.web
    tbot.web.main() 

if __name__ == "__main__":
    irc()