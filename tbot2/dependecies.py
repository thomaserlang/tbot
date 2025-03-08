from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request
from fastapi.security import OAuth2, SecurityScopes

from tbot2.common import TokenData

from .database import database


async def get_session():
    async with database.session() as session:
        yield session
        await session.commit()


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


# token_data: Annotated[TokenData, Security(authenticated, scopes=['SCOPE'])]
async def authenticated(
    security_scopes: SecurityScopes,
    token_data: Annotated[TokenData, Depends(get_token_data)],
):
    if security_scopes.scopes and not token_data.has_any_scope(security_scopes.scopes):  # type: ignore
        raise
    return token_data
