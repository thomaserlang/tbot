from urllib.parse import urljoin

from tbot2.config_settings import config
from tbot2.twitch.http_client import twitch_app_client


async def register_eventsubs(channel_id: str, bot_user_id: str):
    await register_channel_chat_message(channel_id=channel_id, bot_user_id=bot_user_id)


async def register_channel_chat_message(channel_id: str, bot_user_id: str):
    await asyncio.gather(
        _register_eventsub(
            event_type='channel.chat.message',
            version='1',
            condition={'broadcaster_user_id': channel_id, 'user_id': bot_user_id},
        ),
    )


async def _register_eventsub(event_type: str, version: str, condition: dict[str, str]):
    response = await twitch_app_client.post(
        url='/eventsub/subscriptions',
        json={
            'type': event_type,
            'version': version,
            'condition': condition,
            'transport': {
                'method': 'webhook',
                'callback': urljoin(
                    config.web.base_url, f'/twitch/eventsub/{event_type}'
                ),
                'secret': config.twitch.eventsub_secret,
            },
        },
    )
    if response.status_code >= 400:
        raise Exception(response.text)
    return response.json()


if __name__ == '__main__':
    import asyncio

    asyncio.run(register_eventsubs('36981191', '223487116'))
