import pytest
from httpx import AsyncClient

from tbot2.channel_provider import (
    ChannelProviderCreate,
    create_channel_provider,
    get_channel_provider,
)
from tbot2.channel_stream import (
    add_viewer_count,
    create_channel_provider_stream,
    get_channel_provider_stream,
)
from tbot2.common import datetime_now
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_add_viewer_count(client: AsyncClient) -> None:
    user = await user_signin(client, scopes=[])

    channel_provider = await create_channel_provider(
        channel_id=user.channel.id,
        data=ChannelProviderCreate(
            provider='twitch',
            provider_user_id='12345',
        ),
    )

    channel_provider_stream = await create_channel_provider_stream(
        channel_id=user.channel.id,
        provider='twitch',
        provider_user_id='12345',
        provider_stream_id='12345',
        started_at=datetime_now(),
    )

    await add_viewer_count(
        channel_provider_id=channel_provider.id,
        channel_provider_stream_id=channel_provider_stream.id,
        viewer_count=10,
    )

    channel_provider_stream = await get_channel_provider_stream(
        channel_provider_stream_id=channel_provider_stream.id,
    )
    assert channel_provider_stream
    assert channel_provider_stream.avg_viewer_count == 10
    assert channel_provider_stream.peak_viewer_count == 10

    channel_provider = await get_channel_provider(
        channel_id=user.channel.id,
        provider='twitch',
    )
    assert channel_provider
    assert channel_provider.channel_provider_stream_id
    assert channel_provider.channel_provider_stream_id == channel_provider_stream.id
    assert channel_provider.stream_viewer_count == 10


if __name__ == '__main__':
    run_file(__file__)
