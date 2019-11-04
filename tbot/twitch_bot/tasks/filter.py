import logging, re
from ..bot_base import bot
from .. import filters

@bot.on('PRIVMSG')
async def message(nick, target, message, **kwargs):
    filters_ = (
        filters.link.check,
        filters.non_latin.check,
        filters.symbol.check,
        filters.paragraph.check,
        filters.banned_words.check,
        filters.caps.check,
        filters.emote.check,
        filters.action.check,
    )
    for f in filters_:
        try:
            if await f(target, message, kwargs):
                return True
        except:
            logging.exception('filter')