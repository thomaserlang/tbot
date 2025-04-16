from datetime import timedelta
from typing import Any

import jwt
from fastapi.security.utils import get_authorization_scheme_param
from starlette.authentication import AuthCredentials, AuthenticationBackend
from starlette.requests import HTTPConnection

from tbot2.common import TokenData, datetime_now
from tbot2.config_settings import config


class AuthBackend(AuthenticationBackend):
    """
    Own Auth Backend based on Starlette's AuthenticationBackend.

    Use instance of this class as `backend` argument to `add_middleware` func:

    .. code-block:: python

        app = FastAPI()

        @app.on_event('startup')
        async def startup():
            app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())

    """

    async def authenticate(
        self, conn: HTTPConnection
    ) -> tuple[AuthCredentials, TokenData] | None:
        authorization = conn.headers.get('Authorization')
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != 'bearer':
            return None

        try:
            payload = jwt.decode(
                credentials,
                config.secret,
                algorithms=['HS256'],
            )
            token_data = TokenData.model_validate_json(payload['context'])
            return AuthCredentials(token_data.scopes), token_data
        except jwt.PyJWTError:
            return None


async def create_token_str(token_data: TokenData) -> str:
    payload: dict[str, Any] = {
        'context': token_data.model_dump_json(),
        'exp': datetime_now() + timedelta(hours=12),
    }
    return jwt.encode(payload, config.secret, algorithm='HS256')
