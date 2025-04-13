from collections.abc import AsyncGenerator
from urllib.parse import urljoin
from uuid import UUID

from loguru import logger

from tbot2.bot_providers import BotProvider
from tbot2.channel import (
    ChannelOAuthProvider,
    get_channel_bot_provider,
    get_channel_oauth_provider,
    get_channels_providers,
    on_delete_channel_oauth_provider,
    on_disconnect_channel_bot_provider,
)
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


async def register_channel_eventsubs(
    channel_id: UUID,
    event_type: str | None = None,
) -> None:
    logger.info(f'Registering eventsub for channel {channel_id}')
    provider = await get_channel_oauth_provider(
        channel_id=channel_id,
        provider='twitch',
    )
    if not provider:
        logger.error(
            f'Failed to register eventsub for channel {channel_id}: '
            'no oauth provider found'
        )
        return

    bot_provider = provider.bot_provider

    if not bot_provider:
        bot_provider = await get_channel_bot_provider(
            channel_id=channel_id,
            provider='twitch',
        )
        if not bot_provider:
            logger.error(
                f'Failed to register eventsub for channel {channel_id}: '
                'no bot provider found'
            )
            return

    registrations = get_eventsub_registrations(
        broadcaster_user_id=provider.provider_user_id or '',
        twitch_bot_user_id=bot_provider.provider_user_id or '',
    )
    for registration in registrations:
        if event_type and registration.event_type != event_type:
            continue
        try:
            await _register_eventsub(
                registration=registration,
                channel_id=channel_id,
            )
        except Exception as e:
            logger.error(f'Failed to register eventsub {registration.event_type}: {e}')


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
        logger.error(
            f'delete_eventsub_registration: {response.status_code} {response.text}'
        )
        return False
    return True


async def get_eventsubs(
    event_type: str | None = None,
    status: str | None = None,
) -> AsyncGenerator[list[EventSubSubscription]]:
    params: dict[str, str] = {}
    if event_type:
        params['type'] = event_type
    if status:
        params['status'] = status
    response = await twitch_app_client.get(
        url='/eventsub/subscriptions',
        params=params,
    )
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    return get_twitch_pagination_yield(response, EventSubSubscription)


async def unregister_all_eventsubs(event_type: str | None = None) -> None:
    logger.info(f'Unregistering {event_type or "all"} eventsub registrations')
    async for eventsubs in await get_eventsubs(
        event_type=event_type,
    ):
        for eventsub in eventsubs:
            try:
                logger.info(f'Deleting eventsub registration {eventsub.id}')
                await delete_eventsub_registration(eventsub.id)
            except Exception as e:
                logger.error(
                    f'Failed to delete eventsub registration {eventsub.id}: {e}'
                )


async def unregister_channel_eventsubs(
    channel_id: UUID,
    event_type: str | None = None,
) -> None:
    logger.info(
        f'Unregistering {event_type or "all"} eventsub registrations '
        f'for channel {channel_id}'
    )
    channel_id_str = str(channel_id)
    async for eventsubs in await get_eventsubs(
        event_type=event_type,
    ):
        for eventsub in eventsubs:
            if channel_id_str not in eventsub.transport.callback:
                continue
            try:
                logger.info(f'Deleting eventsub registration {eventsub.id}')
                await delete_eventsub_registration(eventsub.id)
            except Exception as e:
                logger.info(
                    f'Failed to delete eventsub registration {eventsub.id}: {e}'
                )


async def register_all_eventsubs(
    event_type: str | None = None,
) -> None:
    logger.info(f'Registering {event_type or "all"} eventsub registrations')
    async for provider in get_channels_providers(provider='twitch'):
        logger.info(f'Registering eventsub for channel {provider.channel_id}')
        await register_channel_eventsubs(
            channel_id=provider.channel_id, event_type=event_type
        )


async def refresh_all_eventsubs(
    event_type: str | None = None,
) -> None:
    await unregister_all_eventsubs(event_type=event_type)
    await register_all_eventsubs(event_type=event_type)


async def refresh_channel_eventsubs(
    channel_id: UUID,
    event_type: str | None = None,
) -> None:
    await unregister_channel_eventsubs(channel_id=channel_id, event_type=event_type)
    await register_channel_eventsubs(channel_id=channel_id, event_type=event_type)


@on_disconnect_channel_bot_provider()
async def handle_disconnect_channel_bot_provider(
    channel_id: UUID,
    bot_provider: BotProvider,
) -> None:
    if bot_provider.provider != 'twitch':
        return
    await refresh_channel_eventsubs(
        channel_id=channel_id, event_type='channel.chat.message'
    )


@on_delete_channel_oauth_provider()
async def handle_delete_channel_oauth_provider(
    channel_provider: ChannelOAuthProvider,
) -> None:
    if channel_provider.provider != 'twitch':
        return
    await unregister_channel_eventsubs(
        channel_id=channel_provider.channel_id,
    )
