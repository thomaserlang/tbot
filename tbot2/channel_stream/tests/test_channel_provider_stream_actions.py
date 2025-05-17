import pytest
from httpx import AsyncClient

from tbot2.channel_provider import ChannelProviderCreate, create_channel_provider
from tbot2.channel_stream import (
    create_channel_provider_stream,
    end_channel_provider_stream,
)
from tbot2.common import datetime_now
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_create_channel_provider_stream(client: AsyncClient) -> None:
    user = await user_signin(client, scopes=[])

    await create_channel_provider(
        channel_id=user.channel.id,
        data=ChannelProviderCreate(
            provider='twitch',
            provider_user_id='12345',
        ),
    )

    result = await create_channel_provider_stream(
        channel_id=user.channel.id,
        provider='twitch',
        provider_user_id='12345',
        provider_stream_id='12345',
        started_at=datetime_now(),
    )
    assert result is not None
    assert result.id is not None
    assert result.channel_id == user.channel.id

    stream = await end_channel_provider_stream(
        channel_id=user.channel.id,
        provider='twitch',
        provider_user_id='12345',
    )
    assert stream is not None
    assert stream.id == result.id
    assert stream.channel_id == user.channel.id
    assert stream.provider == 'twitch'
    assert stream.provider_user_id == '12345'
    assert stream.provider_stream_id == '12345'
    assert stream.started_at == result.started_at
    assert stream.ended_at is not None


if __name__ == '__main__':
    run_file(__file__)
