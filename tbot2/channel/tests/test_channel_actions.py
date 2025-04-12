import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_channel_actions(db: None) -> None:
    channel = await create_channel(data=ChannelCreate(display_name='test'))
    assert channel.display_name == 'test'


if __name__ == '__main__':
    run_file(__file__)
