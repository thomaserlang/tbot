from httpx import Request, Response

from .schemas.error_schema import SubError


class TBotBaseException(Exception):
    def __init__(
        self,
        message: str,
        type: str = '',
        code: int = 500,
        errors: list[SubError] | None = None,
    ) -> None:
        super().__init__(message)
        self.errors = errors or []
        self.message = message
        self.type = type
        self.code = code


class ErrorMessage(TBotBaseException): ...


class ExternalApiError(ErrorMessage):
    def __init__(
        self,
        message: str,
        *,
        request: Request,
        response: Response,
        type: str = 'external_api_error',
        code: int | None = None,
        errors: list[SubError] | None = None,
    ) -> None:
        super().__init__(
            message or f'External API error: {response.status_code}: {response.url}',
            type=type,
            code=code or response.status_code,
            errors=errors,
        )
        self.request = request
        self.response = response
