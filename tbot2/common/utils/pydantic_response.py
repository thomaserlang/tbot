from fastapi.exceptions import RequestValidationError

from ..schemas.error_schema import Error, SubError


def request_validation_error_to_error(exc: RequestValidationError) -> Error:
    """
    Convert a RequestValidationError to an Error object.
    """
    return Error(
        code=422,
        message=_error_message(exc),
        type='validation_error',
        errors=[
            SubError(
                field='.'.join([str(s) for s in e['loc'][1:]]),
                message=rewrite_sub_error_message(e['msg']),
                type=e['type'],
                input=e['input'],
            )
            for e in exc.errors()
        ],
    )


def _error_message(exc: RequestValidationError) -> str:
    for error in exc.errors():
        return (
            f'{".".join([str(s) for s in error["loc"][1:]])}: '
            f'{rewrite_sub_error_message(error["msg"])}'
        )
    return 'One or more fields failed validation'


def rewrite_sub_error_message(
    message: str,
) -> str:
    return message.replace('String', '')
