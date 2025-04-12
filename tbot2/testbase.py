from typing import Any, TypeVar

from attr import dataclass
from httpx import AsyncClient

from tbot2.auth_backend import create_token_str
from tbot2.channel import (
    Channel,
    ChannelCreate,
    create_channel,
    set_channel_user_access_level,
)
from tbot2.common import TAccessLevel, TokenData, TScope
from tbot2.user import User, UserCreate, create_user

T = TypeVar('T')


@dataclass(slots=True)
class TestUser:
    user: User
    channel: Channel


async def user_signin(
    client: AsyncClient | None,
    scopes: list[str | TScope],
) -> TestUser:
    user = await create_user(
        data=UserCreate(
            email='test@example.net',
            display_name='Test User',
            username='testuser',
        )
    )
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )
    await set_channel_user_access_level(
        channel_id=channel.id,
        user_id=user.id,
        access_level=TAccessLevel.OWNER,
    )

    token_str = await create_token_str(
        token_data=TokenData(
            scopes=scopes,
            user_id=user.id,
        )
    )
    if client:
        client.headers.update({'Authorization': f'Bearer {token_str}'})
    return TestUser(
        user=user,
        channel=channel,
    )


def parse_obj_as(type: type[T], obj: Any) -> T:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(type)
    return adapter.validate_python(obj)


def run_file(file_: str) -> None:
    import subprocess

    subprocess.call(['pytest', '--tb=short', str(file_)])
