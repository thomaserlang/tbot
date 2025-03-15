import pytest
from httpx import AsyncClient

from tbot2.channel_quotes import ChannelQuoteCreate, ChannelQuoteUpdate
from tbot2.channel_quotes.types import TChannelQuoteScope
from tbot2.testbase import create_channel_test, run_file, user_signin


@pytest.mark.asyncio
async def test_channel_quote_routes(client: AsyncClient):
    user = await user_signin(
        client,
        scopes=[TChannelQuoteScope.READ, TChannelQuoteScope.WRITE],
    )
    channel = await create_channel_test()

    response = await client.get(f'/api/2/channels/{channel.id}/quotes')
    assert response.status_code == 200

    # Create a quote
    response = await client.post(
        f'/api/2/channels/{channel.id}/quotes',
        json=ChannelQuoteCreate(
            message='Test quote',
            provider='test',
            created_by_chatter_id=str(user.id),
            created_by_display_name=user.display_name,
        ).model_dump(),
    )
    assert response.status_code == 201
    quote = response.json()
    assert quote['message'] == 'Test quote'

    # Get the quote by ID
    response = await client.get(
        f'/api/2/channels/{channel.id}/quotes/{quote["id"]}',
    )
    assert response.status_code == 200
    quote_data = response.json()
    assert quote_data['message'] == 'Test quote'

    # Get the quote by number
    response = await client.get(
        f'/api/2/channels/{channel.id}/quotes/number/1',
    )
    assert response.status_code == 200
    quote_data = response.json()
    assert quote_data['message'] == 'Test quote'

    # Update the quote
    response = await client.put(
        f'/api/2/channels/{channel.id}/quotes/{quote["id"]}',
        json=ChannelQuoteUpdate(
            message='Updated quote',
        ).model_dump(exclude_unset=True),
    )
    assert response.status_code == 200, response.text
    updated_quote = response.json()
    assert updated_quote['message'] == 'Updated quote'
    assert updated_quote['id'] == quote['id']

    # Create another quote
    response = await client.post(
        f'/api/2/channels/{channel.id}/quotes',
        json=ChannelQuoteCreate(
            message='Another quote',
            provider='test',
            created_by_chatter_id=str(user.id),
            created_by_display_name=user.display_name,
        ).model_dump(),
    )
    assert response.status_code == 201
    quote2 = response.json()
    assert quote2['message'] == 'Another quote'
    assert quote2['number'] == 2

    response = await client.delete(
        f'/api/2/channels/{channel.id}/quotes/{quote["id"]}',
    )
    assert response.status_code == 204

    response = await client.get(
        f'/api/2/channels/{channel.id}/quotes/{quote["id"]}',
    )
    assert response.status_code == 404

    # Test number changed
    response = await client.get(
        f'/api/2/channels/{channel.id}/quotes/{quote2["id"]}',
    )
    assert response.status_code == 200
    quote_data = response.json()
    assert quote_data['number'] == 1

    # Test random number
    response = await client.get(
        f'/api/2/channels/{channel.id}/quotes/random',
    )
    assert response.status_code == 200
    quote_data = response.json()
    assert quote_data['message'] == 'Another quote'
    assert quote_data['number'] == 1


if __name__ == '__main__':
    run_file(__file__)
