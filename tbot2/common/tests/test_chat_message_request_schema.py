from uuid6 import uuid7

from tbot2.common import ChatMessageRequest
from tbot2.testbase import run_file


def test_chat_message_request_schema() -> None:
    msg = ChatMessageRequest(
        type='message',
        channel_id=uuid7(),
        provider_viewer_id='123',
        viewer_name='test_user',
        viewer_display_name='TestUser',
        message='Test',
        msg_id='123',
        provider='twitch',
        provider_id='123',
    )
    assert msg.parts
    assert msg.parts[0].text == 'Test'

    msg.type = 'notice'
    msg.notice_message = 'Some notice message'
    assert msg.notice_parts
    assert msg.notice_parts[0].text == 'Some notice message'


if __name__ == '__main__':
    run_file(__file__)
