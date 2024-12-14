from typing import Annotated

from pydantic import BaseModel, StringConstraints


class Oauth2AuthorizeParams(BaseModel):
    client_id: Annotated[str, StringConstraints(min_length=1)]
    redirect_uri: Annotated[str, StringConstraints(min_length=1)]
    response_type: Annotated[str, StringConstraints(min_length=1)] = 'code'
    scope: Annotated[str, StringConstraints(min_length=1)]


class Oauth2AuthorizeResponse(BaseModel):
    code: Annotated[str, StringConstraints(min_length=1)]
    scope: Annotated[str, StringConstraints(min_length=1)]


class Oauth2TokenParams(BaseModel):
    client_id: Annotated[str, StringConstraints(min_length=1)]
    client_secret: Annotated[str, StringConstraints(min_length=1)]
    code: Annotated[str, StringConstraints(min_length=1)]
    grant_type: Annotated[str, StringConstraints(min_length=1)] = 'authorization_code'
    redirect_uri: Annotated[str, StringConstraints(min_length=1)]


class Oauth2TokenResponse(BaseModel):
    access_token: Annotated[str, StringConstraints(min_length=1)]
    refresh_token: Annotated[str, StringConstraints(min_length=1)]
    scope: Annotated[str, StringConstraints(min_length=1)]
    token_type: Annotated[str, StringConstraints(min_length=1)]
    expires_in: int
