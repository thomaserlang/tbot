import pytest

from tbot2.channel import ChannelCreate, create_channel
from tbot2.command import CommandCreate, CommandUpdate, create_command, update_command
from tbot2.testbase import run_file


@pytest.mark.asyncio
async def test_command_actions(db: None):
    channel = await create_channel(
        data=ChannelCreate(
            display_name='test',
        )
    )
    cmd = await create_command(
        channel_id=channel.id,
        data=CommandCreate(
            cmd='test',
            response='test response',
        ),
    )
    assert cmd.cmd == 'test'
    assert cmd.response == 'test response'

    cmd = await update_command(
        command_id=cmd.id,
        data=CommandUpdate(
            cmd='test2',
        ),
    )
    assert cmd.cmd == 'test2'


if __name__ == '__main__':
    run_file(__file__)
