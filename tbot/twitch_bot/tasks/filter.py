import logging, re
from tbot.twitch_bot.bot_base import bot
from tbot.twitch_bot import filters

@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):

    if await filters.link.check(target, message, kwargs):
        return
    if await filters.symbol.check(target, message, kwargs):
        return
    if await filters.paragraph.check(target, message, kwargs):
        return