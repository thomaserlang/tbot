from typing import Annotated
from uuid import UUID

from fastapi import Depends, Header, HTTPException, Path, Request
from fastapi.security import (
    OAuth2,
    SecurityScopes,
)

from tbot2.common import TokenData

oauth2_scheme = OAuth2(auto_error=False)


async def get_token_data(
    request: Request,
    _: Annotated[str, Depends(oauth2_scheme)],
    # To add the authorization header to the documentation
    authorization: Annotated[str, Header(name='Authorization', examples=['Bearer 123'])]
    | None = None,
) -> TokenData:
    if not request.user:
        raise HTTPException(status_code=401, detail='Not authenticated')
    return request.user


async def authenticated(
    security_scopes: SecurityScopes,
    token_data: Annotated[TokenData, Depends(get_token_data)],
):
    """
    Usage: token_data: Annotated[TokenData, Security(authenticated, scopes=['SCOPE'])]
    """
    if security_scopes.scopes and not token_data.has_any_scope(security_scopes.scopes):  # type: ignore
        raise HTTPException(status_code=403, detail='Not enough permissions')
    return token_data


async def auth_channel(
    security_scopes: SecurityScopes,
    channel_id: Annotated[UUID, Path()],
    token_data: Annotated[TokenData, Depends(get_token_data)],
):
    """
    Usage: token_data: Annotated[TokenData, Security(auth_channel, scopes=['SCOPE'])]
    """
    if not await token_data.is_valid_for_channel(channel_id):
        raise HTTPException(status_code=403, detail='Not authorized for this channel')
    return token_data
