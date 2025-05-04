
import pytest
from uuid6 import uuid7

from tbot2.channel_command import CommandCreate, create_command, handle_message_response
from tbot2.channel_command import var_fillers as var_fillers
from tbot2.common import ChatMessageRequest, datetime_now
from tbot2.testbase import run_file, user_signin


@pytest.mark.asyncio
async def test_handle_message(db: None) -> None:
    user = await user_signin(client=None, scopes=[])

    cmd = await create_command(
        channel_id=user.channel.id,
        data=CommandCreate(
            cmds=['test'],
            patterns=['match it'],
            response='Message from: {sender}',
        ),
    )

    response = await handle_message_response(
        chat_message=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            message='!test',
            channel_id=user.channel.id,
            provider_viewer_id=str(uuid7()),
            viewer_name='test_user',
            viewer_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
    )
    assert response is not None
    assert response.command == cmd
    assert response.response == 'Message from: Test User'

    # test pattern
    response = await handle_message_response(
        chat_message=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            message='asd match bbb it',
            channel_id=user.channel.id,
            provider_viewer_id=str(uuid7()),
            viewer_name='test_user',
            viewer_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
    )
    assert response is not None
    assert response.command.id == cmd.id
    assert response.response == 'Message from: Test User'

    cmd = await create_command(
        channel_id=user.channel.id,
        data=CommandCreate(
            patterns=['bbb?'],
            response='Message from: {sender}',
        ),
    )
    response = await handle_message_response(
        chat_message=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            message='asd bbb? it',
            channel_id=user.channel.id,
            provider_viewer_id=str(uuid7()),
            viewer_name='test_user',
            viewer_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
    )
    assert response is not None
    assert response.command.id == cmd.id
    assert response.response == 'Message from: Test User'

    response = await handle_message_response(
        chat_message=ChatMessageRequest(
            id=uuid7(),
            type='message',
            created_at=datetime_now(),
            message='asd bbb it',
            channel_id=user.channel.id,
            provider_viewer_id=str(uuid7()),
            viewer_name='test_user',
            viewer_display_name='Test User',
            provider='twitch',
            provider_id='123',
            msg_id='123',
        ),
    )
    assert response is None


if __name__ == '__main__':
    run_file(__file__)
