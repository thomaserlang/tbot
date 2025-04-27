from httpx import Request, Response

from tbot2.common.exceptions import ExternalApiError

from .schemas.twitch_error_schema import TwitchError


class TwitchException(ExternalApiError):
    def __init__(self, *, request: Request, response: Response) -> None:
        if 'application/json' in response.headers.get('Content-Type'):
            self.error = TwitchError.model_validate(response.json())
        else:
            self.error = TwitchError(
                status=response.status_code,
                message=f'Error {response.status_code}',
                error=f'Error {response.status_code}',
            )
        super().__init__(self.error.message, request=request, response=response)
