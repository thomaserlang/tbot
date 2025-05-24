import asyncio
from collections.abc import AsyncGenerator
from urllib.parse import urljoin
from uuid import UUID

from loguru import logger

from tbot2.channel_provider import (
    ChannelProvider,
    get_channels_providers,
    on_delete_channel_provider,
    on_disconnect_channel_bot_provider,
)
from tbot2.common.exceptions import ErrorMessage
from tbot2.common.utils.chunk_list import chunk_list
from tbot2.config_settings import config

from ..schemas.event_notification_schema import (
    EventSubRegistration,
    EventSubSubscription,
)
from ..twitch_http_client import (
    get_twitch_pagination_yield,
    twitch_app_client,
)


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
            event_type='channel.chat.notification',
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
        EventSubRegistration(
            event_type='channel.moderate',
            version='2',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
                'moderator_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.update',
            version='2',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.channel_points_custom_reward_redemption.add',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.channel_points_automatic_reward_redemption.add',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.channel_points_custom_reward_redemption.update',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.bits.use',
            version='1',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
            },
        ),
        EventSubRegistration(
            event_type='channel.follow',
            version='2',
            condition={
                'broadcaster_user_id': broadcaster_user_id,
                'moderator_user_id': broadcaster_user_id,
            },
        ),
    ]


async def sync_all_eventsubs() -> None:
    logger.info('Syncing Twitch eventsub registrations')
    eventsubs = await eventsubs_grouped_by_broadcaster()
    async for channel_provider in get_channels_providers(provider='twitch'):
        if channel_provider.scope_needed:
            logger.info(
                f'[{channel_provider.channel_id}] '
                f'Skipping eventsub sync for channel, missing scopes'
            )
        await sync_channel_eventsubs(
            channel_provider=channel_provider,
            eventsubs=eventsubs.get(channel_provider.provider_channel_id or '', []),
        )


async def sync_channel_eventsubs(
    channel_provider: ChannelProvider,
    eventsubs: list[EventSubSubscription] | None = None,
) -> None:
    if not eventsubs:
        eventsubs = await get_channel_eventsubs(
            provider_channel_id=channel_provider.provider_channel_id or '',
            channel_id=channel_provider.channel_id,
        )

    bot_provider = await channel_provider.get_default_or_system_bot_provider()
    registrations = get_eventsub_registrations(
        broadcaster_user_id=channel_provider.provider_channel_id or '',
        twitch_bot_user_id=bot_provider.provider_channel_id,
    )
    subs_to_remove = eventsubs[:]
    to_register: list[EventSubRegistration] = []
    for reg in registrations:
        for sub in eventsubs:
            if reg.event_type != sub.type:
                continue
            if sub.status != 'enabled':
                logger.warning(
                    f'[{channel_provider.channel_id}] Twitch eventsub {sub.id} '
                    f'status: {sub.status}'
                )
                continue

            if (
                all(
                    key in sub.condition and sub.condition[key] == value
                    for key, value in reg.condition.items()
                )
                and reg.version == sub.version
                and sub.transport.callback
                == callback_url(
                    event_type=reg.event_type, channel_id=channel_provider.channel_id
                )
            ):
                subs_to_remove.remove(sub)
                break
        else:
            to_register.append(reg)
    logger.info(
        f'[{channel_provider.channel_id}] Twitch eventsubs: {len(subs_to_remove)} '
        f'to remove, {len(to_register)} to register'
    )
    if subs_to_remove:
        await asyncio.gather(
            *[delete_eventsub_registration(sub.id) for sub in subs_to_remove],
            return_exceptions=True,
        )
    if to_register and not channel_provider.scope_needed:
        await asyncio.gather(
            *[
                register_eventsub(
                    registration=registration,
                    channel_id=channel_provider.channel_id,
                )
                for registration in to_register
            ],
            return_exceptions=True,
        )


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
    user_id: str | None = None,
) -> AsyncGenerator[list[EventSubSubscription]]:
    params: dict[str, str] = {}
    if event_type:
        params['type'] = event_type
    if status:
        params['status'] = status
    if user_id:
        params['user_id'] = user_id
    response = await twitch_app_client.get(url='/eventsub/subscriptions', params=params)
    if response.status_code >= 400:
        raise ErrorMessage(f'{response.status_code} {response.text}')
    return get_twitch_pagination_yield(
        client=twitch_app_client, response=response, response_model=EventSubSubscription
    )


async def unregister_all_eventsubs() -> None:
    logger.info('Unregistering all eventsub registrations')
    async for eventsubs in await get_eventsubs():
        for eventsub in chunk_list(eventsubs, 15):
            eventsub_ids = [eventsub.id for eventsub in eventsub]
            logger.info(f'Deleting eventsub registrations {eventsub_ids}')
            await asyncio.gather(
                *[
                    delete_eventsub_registration(eventsub_id)
                    for eventsub_id in eventsub_ids
                ],
                return_exceptions=True,
            )


async def unregister_channel_eventsubs(
    provider_channel_id: str, channel_id: UUID | None = None
) -> None:
    logger.info('Unregistering all eventsub registrations for channel')
    eventsubs = await get_channel_eventsubs(
        provider_channel_id=provider_channel_id, channel_id=channel_id
    )
    await asyncio.gather(
        *[delete_eventsub_registration(eventsub.id) for eventsub in eventsubs],
        return_exceptions=True,
    )


async def get_channel_eventsubs(
    provider_channel_id: str, channel_id: UUID | None = None
) -> list[EventSubSubscription]:
    eventsubs: list[EventSubSubscription] = []
    async for e in await get_eventsubs(user_id=provider_channel_id):
        eventsubs.extend(
            [
                a
                for a in e
                if (a.condition.get('broadcaster_user_id') == provider_channel_id)
                and (not channel_id or str(channel_id) in a.transport.callback)
            ]
        )
    return eventsubs


async def eventsubs_grouped_by_broadcaster() -> dict[str, list[EventSubSubscription]]:
    eventsubs: list[EventSubSubscription] = []
    async for e in await get_eventsubs():
        eventsubs.extend(e)
    eventsubs_grouped_broadcaster: dict[str, list[EventSubSubscription]] = {}
    for eventsub in eventsubs:
        broadcaster_id = eventsub.condition.get('broadcaster_user_id')
        if not broadcaster_id:
            continue
        eventsubs_grouped_broadcaster.setdefault(broadcaster_id, []).append(eventsub)
    return eventsubs_grouped_broadcaster


def callback_url(
    event_type: str,
    channel_id: UUID,
) -> str:
    return urljoin(
        str(config.twitch.eventsub_callback_base_url or config.base_url),
        f'/api/2/twitch/eventsub/{event_type}?channel_id={channel_id}',
    )


async def register_eventsub(
    registration: EventSubRegistration,
    channel_id: UUID,
) -> None:
    response = await twitch_app_client.post(
        url='/eventsub/subscriptions',
        json={
            'type': registration.event_type,
            'version': registration.version,
            'condition': registration.condition,
            'transport': {
                'method': 'webhook',
                'callback': callback_url(
                    event_type=registration.event_type, channel_id=channel_id
                ),
                'secret': config.twitch.eventsub_secret,
            },
        },
    )
    if response.status_code >= 400:
        logger.error(
            f'register_eventsub: {response.status_code}',
            extra={
                'event_type': registration.event_type,
                'channel_id': channel_id,
                'registration': registration,
                'response': response.text,
            },
        )
    return


@on_disconnect_channel_bot_provider()
async def handle_disconnect_channel_bot_provider(
    channel_provider: ChannelProvider,
) -> None:
    if channel_provider.provider != 'twitch':
        return

    await sync_channel_eventsubs(channel_provider=channel_provider)


@on_delete_channel_provider()
async def handle_delete_channel_provider(
    channel_provider: ChannelProvider,
) -> None:
    if channel_provider.provider != 'twitch':
        return
    if channel_provider.provider_channel_id:
        await unregister_channel_eventsubs(
            provider_channel_id=channel_provider.provider_channel_id,
            channel_id=channel_provider.channel_id,
        )
