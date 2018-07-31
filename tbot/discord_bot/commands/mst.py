import logging
from tbot import utils
from tbot.discord_bot import bot
from random import randint
from datetime import timedelta

@bot.command(description='Sync subscriber roles from twitch. Must have `Manage roles` permission to use.')
async def mst(ctx):
    try:
        await ctx.send('Current time in MST: {}'.format(
            str(timedelta(seconds=randint(0, 86400)))[:5]
        ))
    except:
        logging.exception('msg')