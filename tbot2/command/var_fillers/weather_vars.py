from httpx import AsyncClient

from tbot2.common import ChatMessage
from tbot2.config_settings import config

from ..types import TCommand, TMessageVars
from ..var_filler import fills_vars

weather_client = AsyncClient(base_url='https://api.openweathermap.org/data/2.5')


@fills_vars(
    provider='all',
    vars=(
        'weather.lookup_city',
        'weather.units',
        'weather.description',
        'weather.temp',
        'weather.temp_min',
        'weather.temp_max',
        'weather.humidity',
        'weather.city',
        'weather.wind_speed',
    ),
)
async def weather_vars(chat_message: ChatMessage, command: TCommand, vars: TMessageVars):
    if not config.openweathermap_apikey:
        raise ValueError('`openweathermap_apikey` is missing in the config')

    city = (
        ' '.join(command.args)
        if command.args
        else ' '.join(vars['weather.lookup_city'].args)
    )

    if not city:
        raise ValueError(f'Use !{command.name} <city>')

    units = vars['weather.units'].args[0] if vars['weather.units'].args else 'metric'

    params = {
        'q': city,
        'APPID': config.openweathermap_apikey,
        'units': units,
    }
    response = await weather_client.get('/weather', params=params)
    if response.status_code >= 400:
        raise ValueError('Error fetching weather data')

    data = response.json()
    vars['weather.description'].value = (
        data['weather'][0]['description'] if data['weather'] else 'Unknown'
    )
    vars['weather.temp'].value = data['main']['temp']
    vars['weather.temp_min'].value = data['main']['temp_min']
    vars['weather.temp_max'].value = data['main']['temp_max']
    vars['weather.humidity'].value = data['main']['humidity']
    vars['weather.city'].value = data['name']
    vars['weather.wind_speed'].value = data['wind']['speed']
    vars['weather.lookup_city'].value = ''
    vars['weather.units'].value = ''
