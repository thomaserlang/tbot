from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import (
    OAuth2,
    SecurityScopes,
)

from tbot2.common import TokenData


class PlainResponse(Exception):
    """Used if early return in nedded in a dependency."""

    def __init__(self, status_code: int, content: str) -> None:
        self.status_code = status_code
        self.content = content


oauth2_scheme = OAuth2(auto_error=False)


async def get_token_data(
    request: Request,
    _: Annotated[str, Depends(oauth2_scheme)],
) -> TokenData:
    if not request.user or not request.user.is_authenticated:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return request.user


async def authenticated(
    security_scopes: SecurityScopes,
    token_data: Annotated[TokenData, Depends(get_token_data)],
) -> TokenData:
    """
    Usage: token_data: Annotated[TokenData, Security(authenticated, scopes=['SCOPE'])]
    """
    if security_scopes.scopes and not token_data.has_any_scope(security_scopes.scopes):  # type: ignore
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return token_data
