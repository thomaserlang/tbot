import pytest
from httpx import AsyncClient

from tbot2.bot_providers import (
    BotProviderRequest,
    save_bot_provider,
)
from tbot2.channel import (
    ChannelOAuthProviderRequest,
    get_channel_bot_provider,
    save_channel_oauth_provider,
)
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_bot_provider_actions(client: AsyncClient) -> None:
    user = await user_signin(client=client, scopes=[])

    system_bot_provider = await save_bot_provider(
        data=BotProviderRequest(
            provider='twitch',
            name='System Bot',
            provider_user_id='1111',
            system_default=True,
        ),
    )

    bot_provider = await save_bot_provider(
        data=BotProviderRequest(
            provider='twitch',
            name='Test Bot',
            provider_user_id='123',
        ),
    )

    await save_bot_provider(
        data=BotProviderRequest(
            provider='twitch',
            name='Test Bot 2',
            provider_user_id='55555',
        ),
    )

    check_bot_provider = await get_channel_bot_provider(
        provider='twitch',
        channel_id=user.channel.id,
    )
    assert check_bot_provider is not None
    assert check_bot_provider.name == 'System Bot'
    assert check_bot_provider.id == system_bot_provider.id

    await save_channel_oauth_provider(
        channel_id=user.channel.id,
        provider='twitch',
        data=ChannelOAuthProviderRequest(
            provider_user_id='123',
            bot_provider_id=bot_provider.id,
        ),
    )

    check_bot_provider = await get_channel_bot_provider(
        provider='twitch',
        channel_id=user.channel.id,
    )
    assert check_bot_provider is not None
    assert check_bot_provider.name == 'Test Bot'
    assert check_bot_provider.id == bot_provider.id
    assert check_bot_provider.provider_user_id == '123'


if __name__ == '__main__':
    run_file(__file__)
