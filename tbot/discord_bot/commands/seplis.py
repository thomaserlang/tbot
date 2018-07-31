import logging, discord
from tbot import utils
from tbot.discord_bot import bot
from datetime import datetime
from dateutil.parser import parse

@bot.command(description='Get the next episode of a show')
async def tvshow(ctx, *, title):
    try:
        shows = await request('/shows', {
            'title': title,
        })
        if not shows:
            await ctx.send('No show matching the title "{}"'.format(title))
            return
        show = shows[0]

        embed = discord.Embed()
        embed.colour = discord.colour.Colour.blue()
        embed.title = '{} ({})'.format(show['title'], show['premiered'][:4])
        if show['poster_image']:
            embed.set_thumbnail(url=show['poster_image']['url']+'@.jpg')

        episodes = await request('/shows/{}/episodes'.format(show['id']), {
            'q': 'air_date:>={}'.format(datetime.utcnow().date().isoformat()),
        })
        embed.description = ''
        
        if episodes:
            episode = episodes[0]
            embed.description = '**Next episode**: S{}E{} in {}.\n'.format(
                str(episode['season']).zfill(2),
                str(episode['episode']).zfill(2),
                utils.seconds_to_pretty(
                    (parse(episode['air_datetime']).replace(tzinfo=None) - datetime.utcnow()).total_seconds()
                )
            )

        total_episodes = 0
        for season in show['seasons']:
            total_episodes += season['total']

        embed.description += '**Number of episodes**: {} ({} of watchtime).\n'.format(
            total_episodes, 
            utils.seconds_to_pretty((total_episodes * show['runtime'])*60),
        )

        if show['genres']:
            embed.description += '**Genres**: {}.\n'.format(
                ', '.join(show['genres'])
            )

        await ctx.send(embed=embed)
    except:
        logging.exception('tvshow')

async def request(url, params=None, headers={}):
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