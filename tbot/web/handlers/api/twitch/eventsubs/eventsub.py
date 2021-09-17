import logging, asyncio, hmac, hashlib, aiohttp
from os import EX_CANTCREAT
from tbot.utils.twitch import twitch_request
from urllib.parse import urljoin
from tornado import web, escape
from ...base import Api_handler, Api_exception
from tbot import db, utils, config

def channel_events(channel_id):
    events = [
        'channel.goal.begin',
        'channel.goal.progress',
        'channel.goal.end',
    ]
    r = []
    for e in events:
        r.append({
            'type': e,
            'version': '1',
            'condition': {
                'broadcaster_user_id': channel_id,
            },
            'transport': {
                'method': 'webhook',
                'callback': urljoin(config['web']['base_url'], f'/api/twitch/webhooks/{e}'),
                'secret': config['twitch']['eventsub_secret'],
            },
        })
    return r

class Handler(Api_handler):

    async def post(self):
        t = self.request.headers.get('Twitch-Eventsub-Message-Type', None)
        if not t:
            raise web.HTTPError(400, 'Missing Twitch-Eventsub-Message-Type')
        self.verify_signature()
        if t == 'webhook_callback_verification_pending':
            self.set_status(204)
        elif t == 'webhook_callback_verification':
            self.write(self.request.body['challenge'])
        elif t == 'notification':
            await self.notification()
        else:
            raise web.HTTPError(400, 'Unknown')

    def verify_signature(self):
        message = self.request.headers['Twitch-Eventsub-Message-Id'] + \
                self.request.headers['Twitch-Eventsub-Message-Timestamp'] + \
                escape.to_unicode(self.request.original_body)
        signature = 'sha256='+hmac.new(
            key=config['twitch']['eventsub_secret'].encode('utf-8'),
            msg=message.encode('utf-8'),
            digestmod=hashlib.sha256,
        ).hexdigest()
        if self.request.headers['Twitch-Eventsub-Message-Signature'] != signature:
            raise web.HTTPError(400, 'Invalid signature. What are you up to?')

    async def notification(self):
        pass

async def create_eventsubs(ahttp, channel_id, events=None):
    if not events:
        events = channel_events(channel_id)
    url = urljoin(config['twitch']['eventsub_host'], '/helix/eventsub/subscriptions')
    tasks = []
    for e in events:
        tasks.append(utils.twitch_request(ahttp, url, method='POST', json=e, raise_exception=False))
    await asyncio.gather(*tasks)

async def delete_eventsubs(ahttp, ids):
    url = urljoin(config['twitch']['eventsub_host'], '/helix/eventsub/subscriptions')
    tasks = []
    for i in ids:
        tasks.append(utils.twitch_request(ahttp, url, method='DELETE', params={'id': i}, raise_exception=False))
    await asyncio.gather(*tasks)

async def get_all_eventsubs(ahttp):
    after = ''
    url = urljoin(config['twitch']['eventsub_host'], '/helix/eventsub/subscriptions')
    esubs = []
    while True:
        d = await utils.twitch_request(ahttp, url, params={
            'after': after,
        })
        if d['data']:
            esubs.extend(d['data'])
        else:
            break
        if not 'pagination' in d or not d['pagination']:
            break
        after = d['pagination']['cursor']
    return esubs

async def task_check_channels():
    from tbot import db
    db = await db.Db().connect(None)
    try:
        channels = await db.fetchall('SELECT channel_id FROM twitch_channels WHERE active="Y" AND not isnull(twitch_scope);')
        async with aiohttp.ClientSession() as ahttp:
            esubs = await get_all_eventsubs(ahttp)
            grouped = {}
            for e in esubs:
                if 'broadcaster_user_id' in e['condition']:
                    g = grouped.setdefault(e['condition']['broadcaster_user_id'], [])
                    g.append(e)
            for c in channels:
                to_add = []
                to_delete = []
                cevents = channel_events(c['channel_id'])
                eevents = grouped.get(c['channel_id'], [])
                for a in cevents:
                    for e in eevents:
                        if a['type'] == e['type']:
                            if e['status'] == 'enabled' and \
                                e['transport']['callback'] == a['transport']['callback']:
                                break
                            else:
                                to_delete.append(e['id'])
                    else:
                        to_add.append(a)
                if to_delete:
                    await delete_eventsubs(ahttp, to_delete)
                if to_add:
                    await create_eventsubs(ahttp, c['channel_id'], events=to_add)
    finally:
        db.pool.close()
        await db.pool.wait_closed()
