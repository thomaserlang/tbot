import base64
import json
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    StringConstraints,
    field_serializer,
    field_validator,
)


class Oauth2AuthorizeParams(BaseModel):
    client_id: Annotated[str, StringConstraints(min_length=1)]
    redirect_uri: Annotated[str, StringConstraints(min_length=1)]
    response_type: Annotated[str, StringConstraints(min_length=1)] = 'code'
    scope: Annotated[str, StringConstraints(min_length=1)]
    state: dict[str, Any] = {}
    claims: dict[str, str] | None = None

    @field_serializer('state')
    def serialize_state(self, value: dict[str, Any]):
        return base64.b64encode(json.dumps(value).encode('utf-8')).decode('utf-8')

    @field_serializer('claims')
    def serialize_claims(self, value: dict[str, str] | None):
        if value is None:
            return None

        return json.dumps(value).encode('utf-8')


class Oauth2AuthorizeResponse(BaseModel):
    code: Annotated[str, StringConstraints(min_length=1)]
    scope: Annotated[str, StringConstraints(min_length=1)]
    state: dict[str, Any]

    @field_validator('state', mode='before')
    def validate_state(cls, value: str | dict[str, Any]):
        result: dict[str, Any] = {}

        if isinstance(value, str):
            result = json.loads(base64.b64decode(value).decode('utf-8'))

        return result


class Oauth2TokenParams(BaseModel):
    client_id: Annotated[str, StringConstraints(min_length=1)]
    client_secret: Annotated[str, StringConstraints(min_length=1)]
    code: Annotated[str, StringConstraints(min_length=1)]
    grant_type: Annotated[str, StringConstraints(min_length=1)] = 'authorization_code'
    redirect_uri: Annotated[str, StringConstraints(min_length=1)]


class Oauth2TokenResponse(BaseModel):
    access_token: Annotated[str, StringConstraints(min_length=1)]
    refresh_token: Annotated[str, StringConstraints(min_length=1)]
    scope: list[Annotated[str, StringConstraints(min_length=1)]]
    token_type: Annotated[str, StringConstraints(min_length=1)]
    expires_in: int
