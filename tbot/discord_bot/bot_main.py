import asyncio, aiohttp
import logging
import discord
from discord.ext import commands
from tbot import config, db
import tbot.discord_bot.tasks
import tbot.discord_bot.functions
from tbot.discord_bot.tasks.chatlog import Chat_log
from tbot.discord_bot.tasks.command import Command

async def main():
    log = logging.getLogger('main')
    log.setLevel('INFO')
    
    intents = discord.Intents.default()
    intents.presences = True
    intents.members = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='>', help=None, intents=intents)
    bot.add_cog(Chat_log(bot))
    bot.add_cog(Command(bot))
    bot.db = await db.Db().connect()
    bot.ahttp = aiohttp.ClientSession()
    
    bot.loop.create_task(tbot.discord_bot.tasks.twitch_sync.twitch_sync(bot))
    bot.loop.create_task(bot.start(config.data.discord.token))
    log.info('Discord bot started')
    await asyncio.Event().wait()
    log.info('Discord bot stopped')