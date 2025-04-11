from pydantic import field_validator

from tbot2.common import BaseSchema


class ConnectUrl(BaseSchema):
    url: str


class RedirectUrl(BaseSchema):
    redirect_to: str = '/'

    @field_validator('redirect_to')
    def validate_redirect_to(cls, value: str) -> str:
        if not value.startswith('/'):
            raise ValueError('Redirect URL must start with /')
        return value
