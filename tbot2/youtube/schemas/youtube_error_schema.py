from tbot2.common import BaseSchema


class YouTubeSubSubError(BaseSchema):
    message: str
    domain: str
    reason: str
    extendedHelp: str


class YouTubeSubError(BaseSchema):
    code: int
    message: str
    errors: list[YouTubeSubSubError]


class YouTubeError(BaseSchema):
    error: YouTubeSubError
