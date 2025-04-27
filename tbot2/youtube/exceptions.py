from httpx import Request, Response

from tbot2.common.exceptions import ExternalApiError

from .schemas.youtube_error_schema import YouTubeError


class YouTubeException(ExternalApiError):
    def __init__(self, *, request: Request, response: Response) -> None:
        if 'application/json' in response.headers.get('Content-Type'):
            self.error = YouTubeError.model_validate(response.json()['error'])
        else:
            self.error = YouTubeError(
                code=response.status_code,
                message=f'Error {response.status_code}',
                errors=[],
            )
        super().__init__(self.error.message, request=request, response=response)
