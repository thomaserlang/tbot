from datetime import UTC, datetime
from typing import Any

import pytest
from uuid6 import uuid7

from tbot2.chatlog.actions.chatlog_action import create_chatlog
from tbot2.common.schemas.chat_message_schema import ChatMessage
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_create_chatlog(db: Any) -> None:
    t = await create_chatlog(
        data=ChatMessage(
            type='message',
            created_at=datetime.now(tz=UTC),
            channel_id=uuid7(),
            chatter_id='test',
            chatter_name='test',
            chatter_display_name='test',
            message='test',
            msg_id='test',
            provider='twitch',
            provider_id='123',
        )
    )
    assert t is True


if __name__ == '__main__':
    run_file(__file__)
