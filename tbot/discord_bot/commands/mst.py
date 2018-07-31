import logging
from tbot import utils
from tbot.discord_bot import bot
from random import randint
from datetime import timedelta

@bot.command()
async def mst(ctx):
    try:
        seconds = randint(0, 86400)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        await ctx.send('Current time in Michelle Summer Time: {}'.format(
            '{:02d}:{:02d}'.format(hours, minutes)
        ))
    except:
        logging.exception('msg')