import click, asyncio, os
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

@cli.command()
def twitch_bot():
    logger.set_logger('twitch_bot.log')
    from tbot.twitch_bot import bot_main, modlog

    loop = asyncio.get_event_loop()
    loop.create_task(bot_main.bot.connect())
    loop.create_task(modlog.Pubsub().run())

    loop.run_forever()

@cli.command()
def web():
    logger.set_logger('web.log')
    import tbot.web.app
    tbot.web.app.main() 

@cli.command()
def discord():
    logger.set_logger('discord.log')
    import tbot.discord_bot.bot_main
    tbot.discord_bot.bot_main.main() 

@cli.command()
def upgrade():
    from yoyo import read_migrations
    from yoyo import get_backend

    backend = get_backend('mysql://{}:{}@{}:{}/{}'.format(
        config['mysql']['user'],
        config['mysql']['password'],
        config['mysql']['host'],
        config['mysql']['port'],
        config['mysql']['database'],
    ))
    migrations = read_migrations(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations'))
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))

def main():
    cli()

if __name__ == "__main__":
    main()