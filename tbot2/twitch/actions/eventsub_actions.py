import logging
from collections.abc import AsyncGenerator
from urllib.parse import urljoin
from uuid import UUID

from tbot2.channel import (
    get_channel_bot_provider,
    get_channel_oauth_provider,
    get_channels_providers,
)
from tbot2.common import TProvider
from tbot2.config_settings import config
from tbot2.exceptions import ErrorMessage

from ..schemas.eventsub_notification_schema import (
    EventSubRegistration,
    EventSubSubscription,
)
from ..twitch_http_client import (
    get_twitch_pagination_yield,
    twitch_app_client,
)


async def register_eventsubs(
    channel_id: UUID,
) -> None:
    provider = await get_channel_oauth_provider(
        channel_id=channel_id,
        provider=TProvider.twitch,
    )
    if not provider:
        logging.error(
            f'Failed to register eventsub for channel {channel_id}: '
            'no oauth provider found'
        )
        return

    bot_provider = provider.bot_provider

    if not bot_provider:
        bot_provider = await get_channel_bot_provider(
            channel_id=channel_id,
            provider=TProvider.twitch,
        )
        if not bot_provider:
            logging.error(
                f'Failed to register eventsub for channel {channel_id}: '
                'no bot provider found'
            )
            return

    registrations = get_eventsub_registrations(
        broadcaster_user_id=provider.provider_user_id or '',
        twitch_bot_user_id=bot_provider.provider_user_id or '',
    )
    for registration in registrations:
        try:
            await _register_eventsub(
                registration=registration,
                channel_id=channel_id,
            )
        except Exception as e:
            logging.error(f'Failed to register eventsub {registration.event_type}: {e}')


def get_eventsub_registrations(
    broadcaster_user_id: str,
    twitch_bot_user_id: str,
) -> list[EventSubRegistration]:
    return [
        EventSubRegistration(
            event_type='channel.chat.message',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
                'user_id': twitch_bot_user_id,
            },
        ),
        EventSubRegistration(
            event_type='stream.online',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='stream.offline',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
    ]


async def _register_eventsub(
    registration: EventSubRegistration,
    channel_id: UUID,
) -> EventSubSubscription:
    response = await twitch_app_client.post(
        url='/eventsub/subscriptions',
        json={
            'type': registration.event_type,
            'version': registration.version,
            'condition': registration.condition,
            'transport': {
                'method': 'webhook',
                'callback': urljoin(
                    str(
                        config.twitch.eventsub_callback_base_url or config.web.base_url
                    ),
                    f'/api/2/twitch/eventsub/{registration.event_type}?channel_id={channel_id}',
                ),
                'secret': config.twitch.eventsub_secret,
            },
        },
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    return EventSubSubscription.model_validate(response.json()['data'][0])


async def delete_eventsub_registration(event_id: str) -> bool:
    response = await twitch_app_client.delete(
        url=f'/eventsub/subscriptions?id={event_id}'
    )
    if response.status_code >= 400:
        logging.error(
            f'delete_eventsub_registration: {response.status_code} {response.text}'
        )
        return False
    return True


async def get_eventsubs(
    type: str | None = None,
    status: str | None = None,
) -> AsyncGenerator[list[EventSubSubscription]]:
    params: dict[str, str] = {}
    if type:
        params['type'] = type
    if status:
        params['status'] = status
    response = await twitch_app_client.get(
        url='/eventsub/subscriptions',
        params=params,
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    return get_twitch_pagination_yield(response, EventSubSubscription)


async def unregister_all_eventsubs() -> None:
    async for eventsubs in await get_eventsubs():
        for eventsub in eventsubs:
            try:
                logging.info(f'Deleting eventsub registration {eventsub.id}')
                await delete_eventsub_registration(eventsub.id)
            except Exception as e:
                logging.error(
                    f'Failed to delete eventsub registration {eventsub.id}: {e}'
                )


async def unregister_channel_eventsubs(
    channel_id: UUID,
) -> None:
    async for eventsubs in await get_eventsubs():
        for eventsub in eventsubs:
            if str(channel_id) not in eventsub.transport.callback:
                continue
            try:
                logging.info(f'Deleting eventsub registration {eventsub.id}')
                await delete_eventsub_registration(eventsub.id)
            except Exception as e:
                logging.info(
                    f'Failed to delete eventsub registration {eventsub.id}: {e}'
                )


async def register_all_eventsubs() -> None:
    async for provider in get_channels_providers(provider=TProvider.twitch):
        logging.info(f'Registering eventsub for channel {provider.channel_id}')
        await register_eventsubs(channel_id=provider.channel_id)
