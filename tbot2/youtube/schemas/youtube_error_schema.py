from tbot2.common import BaseSchema


class YouTubeSubError(BaseSchema):
    message: str
    domain: str
    reason: str
    extendedHelp: str | None = None


class YouTubeError(BaseSchema):
    code: int
    message: str
    errors: list[YouTubeSubError]
