import json
from datetime import UTC, datetime, timedelta
from typing import Annotated, Any

import jwt
from fastapi import HTTPException
from loguru import logger
from pydantic import (
    BaseModel,
    StringConstraints,
    field_serializer,
    field_validator,
)

from tbot2.config_settings import config


class Oauth2AuthorizeParams(BaseModel):
    client_id: Annotated[str, StringConstraints(min_length=1)]
    redirect_uri: Annotated[str, StringConstraints(min_length=1)]
    response_type: Annotated[str, StringConstraints(min_length=1)] = 'code'
    scope: Annotated[str, StringConstraints(min_length=1)]
    state: dict[str, Any] = {}
    claims: dict[str, str] | None = None
    force_verify: bool | None = None
    access_type: str | None = None
    include_granted_scopes: bool | None = None
    prompt: str | None = None

    @field_serializer('state')
    def serialize_state(self, value: dict[str, Any]) -> str:
        payload: dict[str, Any] = {
            'context': value,
            'exp': datetime.now(tz=UTC) + timedelta(minutes=5),
        }
        return jwt.encode(payload, config.secret, algorithm='HS256')

    @field_serializer('force_verify', 'include_granted_scopes')
    def validate_force_verify(self, value: bool | None) -> str | None:
        if value is None:
            return None
        return 'true' if value else 'false'

    @field_serializer('claims')
    def serialize_claims(self, value: dict[str, str] | None) -> str:
        if value is None:
            return ''

        return json.dumps(value)


class Oauth2AuthorizeResponse(BaseModel):
    code: Annotated[str, StringConstraints(min_length=1)]
    scope: Annotated[str, StringConstraints(min_length=0)] = ''
    state: dict[str, Any]

    @field_validator('state', mode='before')
    def validate_state(cls, value: str | dict[str, Any]) -> dict[str, Any]:
        result: dict[str, Any] = {}

        if isinstance(value, str):
            try:
                result = jwt.decode(
                    value,
                    config.secret,
                    algorithms=['HS256'],
                )['context']
            except jwt.ExpiredSignatureError:
                raise HTTPException(
                    status_code=400,
                    detail='State expired',
                ) from None
            except jwt.PyJWTError:
                raise HTTPException(
                    status_code=400,
                    detail='Invalid state',
                ) from None

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
    token_type: Annotated[str, StringConstraints(min_length=1)]
    expires_in: int
    id_token: dict[str, Any] | None = None

    @field_validator('id_token', mode='before')
    def validate_jwt_token(cls, value: str | None) -> dict[str, Any] | None:
        if value is None:
            return None

        try:
            return jwt.decode(value, options={'verify_signature': False})
        except jwt.PyJWTError as e:
            logger.error(f'Invalid jwt token: {e}')
            raise HTTPException(
                status_code=400,
                detail='Invalid id_token',
            ) from e
