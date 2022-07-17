import click, asyncio, os, logging
from tbot import config, config_load, logger

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
    logger.set_logger('twitch_bot.log', sentry_dsn=config.data.sentry_dsn)
    from tbot.twitch_bot import bot_main, modlog
    log = logging.getLogger('main')
    log.setLevel('INFO')
    log.info('Twitch bot started')
    loop = asyncio.get_event_loop()
    loop.create_task(bot_main.bot.connect())
    loop.create_task(modlog.Pubsub().run())
    loop.run_forever()
    log.info('Twitch bot stopped')

@cli.command()
def web():
    logger.set_logger('web.log', sentry_dsn=config.data.sentry_dsn)
    import tbot.web.app
    tbot.web.app.main() 

@cli.command()
def discord():
    logger.set_logger('discord.log', sentry_dsn=config.data.sentry_dsn)
    import tbot.discord_bot.bot_main
    tbot.discord_bot.bot_main.main() 

@cli.command()
def upgrade():
    logger.set_logger('migration.log', sentry_dsn=config.data.sentry_dsn)
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
    logger.set_logger('twitch_eventsub_check.log', sentry_dsn=config.data.sentry_dsn)
    from tbot.web.handlers.api.twitch.eventsubs.eventsub import task_check_channels
    asyncio.run(task_check_channels())

def main():
    cli()

if __name__ == "__main__":
    main()