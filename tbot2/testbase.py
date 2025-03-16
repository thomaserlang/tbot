from typing import Any, TypeVar

from httpx import AsyncClient

from tbot2.auth_backend import create_token_str
from tbot2.channel import ChannelCreate, create_channel
from tbot2.common import TokenData, TScope
from tbot2.user import UserCreate, create_user

T = TypeVar('T')


async def user_signin(
    client: AsyncClient,
    scopes: list[str | TScope],
):
    user = await create_user(
        data=UserCreate(
            email='test@example.net',
            display_name='Test User',
            username='testuser',
        )
    )
    token_str = await create_token_str(
        token_data=TokenData(
            scopes=scopes,
            user_id=user.id,
        )
    )
    client.headers.update({'Authorization': f'Bearer {token_str}'})
    return user


async def create_channel_test():
    channel = await create_channel(
        data=ChannelCreate(
            display_name='Test Channel',
        )
    )
    return channel


def parse_obj_as(type: type[T], obj: Any) -> T:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(type)
    return adapter.validate_python(obj)


def run_file(file_: str):
    import subprocess

    subprocess.call(['pytest', '--tb=short', str(file_)])
