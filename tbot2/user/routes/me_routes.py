from typing import Annotated

from fastapi import APIRouter, HTTPException, Security

from tbot2.common import TokenData
from tbot2.dependecies import authenticated

from ..actions.user_actions import delete_user, get_user
from ..schemas.user_schema import UserPublic

router = APIRouter()


@router.get('/me')
async def me(token_data: Annotated[TokenData, Security(authenticated)]) -> UserPublic:
    user = await get_user(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='User not found',
        )
    return UserPublic.model_validate(user)


@router.delete('/me', status_code=204)
async def delete_me(
    username: str, token_data: Annotated[TokenData, Security(authenticated)]
) -> None:
    user = await get_user(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found',
        )
    if user.username.lower() != username:
        raise HTTPException(
            status_code=400,
            detail='Username does not match',
        )
    await delete_user(
        user_id=token_data.user_id,
    )
