from typing import Annotated

from fastapi import APIRouter, HTTPException, Security

from tbot2.common import TokenData
from tbot2.dependecies import authenticated

from ..actions.user_actions import get_user
from ..schemas.user_schema import UserPublic

router = APIRouter()


@router.get('/me', response_model=UserPublic)
async def me(token_data: Annotated[TokenData, Security(authenticated)]):
    user = await get_user(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail='User not found',
        )
    return user
