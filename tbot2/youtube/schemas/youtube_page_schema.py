
from typing import Generic, TypeVar

from tbot2.common import BaseSchema

T = TypeVar('T')

class YoutubePage(BaseSchema, Generic[T]):
    items: list[T]
