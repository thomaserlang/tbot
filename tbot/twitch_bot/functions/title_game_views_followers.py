from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils

@fills_vars('title', 'game')
async def get_title_game(bot, channel_id, **kwargs):
    data = await utils.twitch_request(bot.ahttp, 
        f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}',
    )
    if not data['data']:
        raise Send_error('No data')
    return {
        'title': data['data'][0]['title'] or '<No title>',
        'game': data['data'][0]['game_name'] or '<Not in any game category>',
    }

@fills_vars('followers')
async def get_followers(bot, channel_id, **kwargs):
    data = await utils.twitch_channel_token_request(bot.ahttp, channel_id,
        'https://api.twitch.tv/helix/channels/followers',
        params={
            'first': 1,
            'broadcaster_id': channel_id,
        }
    )
    if not data['data']:
        raise Send_error('No data')
    return {
        'followers': str(data['total']),
    }

@fills_vars('set_title')
async def set_title(bot, channel_id, args, var_args, **kwargs):
    title = ' '.join(args) or ' '.join(var_args['set_title'])
    if not title:
        raise Send_error('You must specify a title')
    try:
        await utils.twitch_channel_token_request(
            bot, channel_id,
            f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}',
            method='PATCH',
            json={
                'title': title,
            },
        )
    except utils.Twitch_request_error as e:
        raise Send_error(f'Unable to change title. Error: {str(e)}')
    raise Send_error(f'Title changed to: {title}')

@fills_vars('set_language')
async def set_language(bot, channel_id, args, var_args, **kwargs):
    language = ' '.join(args) or ' '.join(var_args['set_language'])
    if not language:
        raise Send_error('You must specify a language')
    try:
        await utils.twitch_channel_token_request(
            bot, channel_id,
            f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}',
            method='PATCH',
            json={
                'broadcaster_language': language,
            },
        )
    except utils.Twitch_request_error as e:
        raise Send_error(f'Unable to change language. Error: {str(e)}')
    raise Send_error(f'Language changed to: {language}')

@fills_vars('set_delay')
async def set_delay(bot, channel_id, args, var_args, **kwargs):
    delay = ' '.join(args) or ' '.join(var_args['set_delay'])
    try:
        delay = int(delay)
    except ValueError:        
        raise Send_error('Delay must be a number')
    try:
        await utils.twitch_channel_token_request(
            bot, channel_id,
            f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}',
            method='PATCH',
            json={
                'delay': delay,
            },
        )
    except utils.Twitch_request_error as e:
        raise Send_error(f'Unable to change delay. Error: {str(e)}')
    raise Send_error(f'Delay changed to: {delay}')

@fills_vars('set_game')
async def set_game(bot, channel_id, args, var_args, **kwargs):
    game = ' '.join(args) or ' '.join(var_args['set_game'])
    if not game:
        raise Send_error('You must specify a game or a category')
    game_id=''
    if game != '<unset>':
        data = await utils.twitch_channel_token_request(
            bot, channel_id,
            'https://api.twitch.tv/helix/search/categories',
            params={'query': f'"{game}"'},
        )
        if 'data' in data and data['data']:
            for g in data['data']:
                if g['name'].lower() == game.lower():
                    game_id = g['id']
                    game = g['name']
                    break
            else:
                game_id = data['data'][0]['id']
                game = data['data'][0]['name']
        else:
            raise Send_error(f'No game or category found for {game}')
    try:
        await utils.twitch_channel_token_request(
            bot, channel_id,
            f'https://api.twitch.tv/helix/channels?broadcaster_id={channel_id}',
            method='PATCH',
            json={
                'game_id': game_id,
            },
        )
    except utils.Twitch_request_error as e:
        raise Send_error(f'Unable to change game/category. Error: {str(e)}')
    raise Send_error(f'Game/category changed to: {game}')
