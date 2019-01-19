import logging, urllib.parse
from tbot.twitch_bot.var_filler import fills_vars, Send_error
from tbot import utils
from datetime import datetime
from dateutil.parser import parse

@fills_vars('title', 'game', 'views', 'followers')
async def title_game_views_followers(bot, channel_id, **kwargs):
    data = await utils.twitch_request(bot.ahttp, 
        'https://api.twitch.tv/kraken/channels/{}'.format(channel_id),
    )    
    return {
        'title': data['status'] or '<No title>',
        'game': data['game'] or '<Not in any game category>',
        'followers': str(data['followers']),
        'views': str(data['views']),
    }

@fills_vars('set_title')
async def set_title(bot, cmd, channel_id, args, var_args, **kwargs):
    title = ' '.join(args) or ' '.join(var_args['set_title'])
    if not title:
        raise Send_error('You must specify a title')
    try:
        data = await utils.twitch_channel_token_request(
            bot, 
            channel_id,
            'https://api.twitch.tv/kraken/channels/{}'.format(channel_id),
            method='PUT',
            data='channel[status]={}'.format(urllib.parse.quote(
                title
            ))
        )
    except utils.Twitch_request_error as e:
        raise Send_error('Unable to change game. Error: {}'.format(str(e)))
    raise Send_error('Title changed to: {}'.format(data['status']))

@fills_vars('set_game')
async def set_game(bot, cmd, channel_id, args, var_args, **kwargs):
    game = ' '.join(args) or ' '.join(var_args['set_game'])
    if not game:
        raise Send_error('You must specify a game')
    try:
        data = await utils.twitch_channel_token_request(
            bot, 
            channel_id,
            'https://api.twitch.tv/kraken/channels/{}'.format(channel_id),
            method='PUT',
            data='channel[game]={}'.format(urllib.parse.quote(
                game
            ))
        )
    except utils.Twitch_request_error as e:
        raise Send_error('Unable to change game. Error: {}'.format(str(e)))
    raise Send_error('Game changed to: {}'.format(data['game']))