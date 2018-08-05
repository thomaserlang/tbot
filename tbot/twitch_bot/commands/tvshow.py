import logging
from tbot.twitch_bot.command import command
from tbot import config, utils

@command('tvshow')
async def tvshow(bot, nick, channel, channel_id, target, args, **kwargs):
    if len(args) < 1:
        return
    title = ' '.join(args)
    try:
        shows = await request(bot, '/shows', {
            'title': title,
        })
        if not shows:
            bot.send("PRIVMSG", target=target, message='No show matching the title "{}"'.format(title))
            return
        show = shows[0]

        total_episodes = 0
        for season in show['seasons']:
            total_episodes += season['total']

        text = '{} - Number of episodes: {} ({} of watchtime)'.format(
            '{} ({})'.format(show['title'], show['premiered'][:4]),
            total_episodes, 
            utils.seconds_to_pretty((total_episodes * show['runtime'])*60),
        )
        bot.send("PRIVMSG", target=target, message=text)
    except:
        logging.exception('tvshow')

async def request(bot, url, params=None, headers={}):
    url = 'https://api.seplis.net/1'+url
    async with bot.ahttp.get(url, params=params, headers=headers) as r:
        if r.status == 200:
            data = await r.json()
            return data
        else:
            text = await r.text()
            raise Exception('seplis request failed - {}: {}'.format(
                r.status,
                text
            ))