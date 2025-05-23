from typing import Generic, Literal, TypeVar

from tbot2.common import BaseSchema

DataT = TypeVar('DataT')


class PubSubEvent(BaseSchema, Generic[DataT]):
    type: Literal['activity', 'chat_message']
    action: Literal['new', 'updated', 'deleted']
    data: DataT
