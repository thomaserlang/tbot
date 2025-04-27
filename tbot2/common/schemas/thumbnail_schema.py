
from tbot2.common import BaseSchema


class Thumbnail(BaseSchema):
    url: str
    width: int | None = None
    height: int | None = None
