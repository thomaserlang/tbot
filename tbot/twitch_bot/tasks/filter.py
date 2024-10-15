from tbot import logger

from .. import filters
from ..bot_base import bot


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
        except Exception:
            logger.exception('filter')