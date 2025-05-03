from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import (
    OAuth2,
    SecurityScopes,
)

from tbot2.common import ErrorMessage, TokenData


class PlainResponse(Exception):
    """Used if early return is nedded in a dependency"""

    def __init__(self, status_code: int, content: str) -> None:
        self.status_code = status_code
        self.content = content


oauth2_scheme = OAuth2(auto_error=False)


async def get_token_data(
    request: Request,
    _: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    if not request.user or not request.user.is_authenticated:
        raise ErrorMessage(
            code=401,
            message='Not authenticated',
            type='unauthenticated',
        )
    return request.user


async def authenticated(
    security_scopes: SecurityScopes,
    token_data: Annotated[TokenData, Depends(get_token_data)],
) -> TokenData:
    """
    Usage: token_data: Annotated[TokenData, Security(authenticated, scopes=['SCOPE'])]
    """
    if security_scopes.scopes and not token_data.has_any_scope(security_scopes.scopes):  # type: ignore
        raise ErrorMessage(
            code=403,
            message=(
                f'Required scopes: {[str(scope) for scope in security_scopes.scopes]}'
            ),
            type='forbidden',
        )
    return token_data
