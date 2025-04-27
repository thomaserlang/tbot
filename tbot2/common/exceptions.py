from httpx import Request, Response


class TBotBaseException(Exception): ...


class ErrorMessage(TBotBaseException): ...


class ExternalApiError(TBotBaseException):
    def __init__(self, message: str, *, request: Request, response: Response) -> None:
        super().__init__(
            message or f'External API error: {response.status_code}: {response.url}'
        )
        self.request = request
        self.response = response
