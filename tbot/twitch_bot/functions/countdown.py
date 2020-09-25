from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil import tz

@fills_vars('countdown',)
async def countdown(bot, var_args, **kwargs):
    d = ' '.join(var_args['countdown'])
    try:
        dt = parse(d).astimezone(tz.UTC).replace(tzinfo=None)
    except ValueError:
        raise Send_error(f'Invalid date format: "{d}". Use ISO 8601 format.')
    secs = (dt - datetime.utcnow()).total_seconds()
    
    return {
        'countdown': utils.seconds_to_pretty(secs),
    }
  
