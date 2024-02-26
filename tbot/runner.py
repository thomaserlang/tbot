import click, asyncio, os, logging
from tbot import config, config_load, set_logger

@click.group()
@click.option('--config', default=None, help='path to the config file')
@click.option('--log_path', '-lp', default=None, help='a folder to store the log files in')
@click.option('--log_level', '-ll', default=None, help='notset, debug, info, warning, error or critical')
def cli(config, log_path, log_level):
    config_load(config)
    if log_path != None:
        config.data.logging.path = log_path
    if log_level:
        config.data.logging.level = log_level

@cli.command()
def twitch_bot():
    set_logger('twitch_bot.log')
    from tbot.twitch_bot import bot_main
    from tbot.web.handlers.api.twitch.eventsubs.eventsub import task_check_channels
    asyncio.run(task_check_channels())
    asyncio.run(bot_main.main())

@cli.command()
def web():
    set_logger('web.log')
    import tbot.web.app
    asyncio.run(tbot.web.app.main()) 

@cli.command()
def discord():
    set_logger('discord.log')
    import tbot.discord_bot.bot_main
    asyncio.run(tbot.discord_bot.bot_main.main())

@cli.command()
def upgrade():
    set_logger('migration.log')
    from yoyo import read_migrations
    from yoyo import get_backend

    backend = get_backend('mysql://{}:{}@{}:{}/{}'.format(
        config.data.mysql.user,
        config.data.mysql.password,
        config.data.mysql.host,
        config.data.mysql.port,
        config.data.mysql.database,
    ))    
    log = logging.getLogger('main')
    log.setLevel('INFO')
    log.info('Upgrade started')
    migrations = read_migrations(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'migrations'))
    with backend.lock():
        backend.apply_migrations(backend.to_apply(migrations))
    log.info('Upgrade done')

@cli.command()
def twitch_eventsub_check():
    set_logger('twitch_eventsub_check.log')
    from tbot.web.handlers.api.twitch.eventsubs.eventsub import task_check_channels
    asyncio.run(task_check_channels())

def main():
    cli()

if __name__ == "__main__":
    main()