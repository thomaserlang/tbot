from typing import Any, Collection, TypeVar

from httpx import AsyncClient

from tbot2.common import TScope
from tbot2.user import UserCreate, create_user

T = TypeVar('T')


async def user_signin(
    client: AsyncClient,
    scopes: Collection[TScope],
):
    await create_user(
        data=UserCreate(
            username='test_user',
            email='test@example.net',
            display_name='Test User',
        )
    )


def parse_obj_as(type: type[T], obj: Any) -> T:
    from pydantic import TypeAdapter

    adapter = TypeAdapter(type)
    return adapter.validate_python(obj)


def run_file(file_: str):
    import subprocess

    subprocess.call(['pytest', '--tb=short', str(file_)])
