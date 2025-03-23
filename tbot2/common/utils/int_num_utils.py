from enum import Enum
from typing import Type

from sqlalchemy import Integer, TypeDecorator
from sqlalchemy.engine.interfaces import Dialect


class IntEnum(TypeDecorator[Enum | int]):
    """
    Enables passing in a Python enum and storing the enum's *value* in the db.
    The default would have stored the enum's *name* (ie the string).
    """

    impl = Integer

    def __init__(self, enumtype: Type[Enum], *args: object, **kwargs: object) -> None:
        super(IntEnum, self).__init__(*args, **kwargs)
        self._enumtype = enumtype

    def process_bind_param(self, value: Enum | int | None, dialect: Dialect):
        if isinstance(value, Enum):
            return value.value
        return value

    def process_result_value(self, value: int | None, dialect: Dialect):
        return self._enumtype(value)
