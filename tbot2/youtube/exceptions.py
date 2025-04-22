from tbot2.exceptions import InternalHttpError

from .schemas.youtube_error_schema import YouTubeError


class YouTubeException(InternalHttpError):
    def __init__(self, error: YouTubeError) -> None:
        super().__init__(error.error.code, error.error.message)
        self.error = error
