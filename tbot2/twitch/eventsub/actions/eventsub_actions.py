import logging
from urllib.parse import urljoin
from uuid import UUID

from tbot2.config_settings import config
from tbot2.twitch.http_client import get_twitch_pagination, twitch_app_client

from ..schemas.eventsub_notification_schema import (
    EventSubSubscription,
)


async def register_channel_eventsubs(
    channel_id: UUID,
    twitch_channel_id: str,
    twitch_bot_user_id: str,
):
    await register_channel_chat_message(
        channel_id=channel_id,
        twitch_channel_id=twitch_channel_id,
        twitch_bot_user_id=twitch_bot_user_id,
    )


async def register_channel_chat_message(
    channel_id: UUID,
    twitch_channel_id: str,
    twitch_bot_user_id: str,
):
    await _register_eventsub(
        event_type='channel.chat.message',
        version='1',
        condition={
            'broadcaster_user_id': twitch_channel_id,
            'user_id': twitch_bot_user_id,
        },
        channel_id=channel_id,
    )


async def _register_eventsub(
    event_type: str,
    version: str,
    condition: dict[str, str],
    channel_id: UUID,
):
    response = await twitch_app_client.post(
        url='/eventsub/subscriptions',
        json={
            'type': event_type,
            'version': version,
            'condition': condition,
            'transport': {
                'method': 'webhook',
                'callback': urljoin(
                    config.web.base_url,
                    f'/twitch/eventsub/{event_type}?channel_id={channel_id}',
                ),
                'secret': config.twitch.eventsub_secret,
            },
        },
    )
    response.raise_for_status()
    return EventSubSubscription.model_validate_json(response.json())


async def delete_eventsub_registration(event_id: str):
    response = await twitch_app_client.delete(
        url=f'/eventsub/subscriptions?id={event_id}'
    )
    response.raise_for_status()
    return True


async def get_eventsubs(
    type: str | None = None,
    status: str | None = None,
):
    params: dict[str, str] = {}
    if type:
        params['type'] = type
    if status:
        params['status'] = status
    response = await twitch_app_client.get(
        url='/eventsub/subscriptions',
        params=params,
    )
    response.raise_for_status()
    return await get_twitch_pagination(response, schema=EventSubSubscription)


async def unregister_all_eventsubs():
    eventsubs = await get_eventsubs()
    for eventsub in eventsubs:
        try:
            await delete_eventsub_registration(eventsub.id)
        except Exception as e:
            logging.info(f'Failed to delete eventsub registration {eventsub.id}: {e}')


async def unregister_channel_eventsubs(
    channel_id: UUID,
):
    eventsubs = await get_eventsubs()
    for eventsub in eventsubs:
        if str(channel_id) in eventsub.transport.callback:
            try:
                await delete_eventsub_registration(eventsub.id)
            except Exception as e:
                logging.info(
                    f'Failed to delete eventsub registration {eventsub.id}: {e}'
                )


if __name__ == '__main__':
    import asyncio

    asyncio.run(unregister_all_eventsubs())
