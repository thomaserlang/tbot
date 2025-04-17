class BaseException(Exception): ...


class ErrorMessage(BaseException): ...

class InternalHttpError(BaseException):
    def __init__(self, status_code: int, body: str) -> None:
        super().__init__(body)
        self.status_code = status_code
        self.body = body