from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import config

@fills_vars('weather.lookup_city', 'weather.units', 'weather.description', 'weather.temp',
            'weather.temp_min', 'weather.temp_max', 'weather.humidity', 
            'weather.city', 'weather.wind_speed',)
async def weather(bot, var_args, args, cmd, **kwargs):
    if not config.data.openweathermap_apikey:
        raise Send_error('`openweathermap_apikey` is missing in the config')
    url = 'https://api.openweathermap.org/data/2.5/weather'
    city = None
    if len(args) > 0:
        city = ' '.join(args)
    if not city:
        city = ' '.join(var_args.get('weather.lookup_city', ['']))

    if not city:
        raise Send_error(f'Use !{cmd} <city>')

    units = var_args.get('weather.units', ['metric'])[0]

    params = {
        'q': city,
        'APPID': config.data.openweathermap_apikey,
        'units': units,
    } 
    async with bot.ahttp.get(url, params=params) as r:
        d = await r.json()
        if r.status == 200:
            return {
                'weather.description': d['weather'][0]['description']\
                    if d['weather'] else 'Unknown',
                'weather.temp': d['main']['temp'],
                'weather.temp_min': d['main']['temp_min'],
                'weather.temp_max': d['main']['temp_max'],
                'weather.humidity': d['main']['humidity'],
                'weather.city': d['name'],
                'weather.wind_speed': d['wind']['speed'],
                'weather.lookup_city': '',
                'weather.units': '',
            }
        else:  
            raise Send_error(d['message'])