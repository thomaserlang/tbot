from uuid import UUID

from tbot2.channel.event_types import on_deleting_channel
from tbot2.contexts import AsyncSession

from ..actions.channel_provider_actions import (
    delete_channel_provider,
    get_channel_providers,
)


@on_deleting_channel()
async def handle_deleting_channel(
    channel_id: UUID,
    session: AsyncSession,
) -> None:
    channel_providers = await get_channel_providers(
        channel_id=channel_id,
        session=session,
    )
    for channel_provider in channel_providers:
        await delete_channel_provider(
            channel_provider_id=channel_provider.id,
            session=session,
        )
