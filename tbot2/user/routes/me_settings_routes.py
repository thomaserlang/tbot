from typing import Annotated

from fastapi import APIRouter, Security

from tbot2.common import TokenData
from tbot2.dependecies import authenticated
from tbot2.user.actions.user_settings_actions import (
    get_user_settings,
    update_user_settings,
)
from tbot2.user.schemas.user_settings_schema import UserSettings

router = APIRouter()


@router.get('/me/settings', name='User Settings')
async def get_user_settings_route(
    token_data: Annotated[TokenData, Security(authenticated)],
) -> UserSettings:
    settings = await get_user_settings(user_id=token_data.user_id)
    return UserSettings.model_validate(settings)


@router.put('/me/settings', name='Update User Settings', status_code=204)
async def update_user_settings_route(
    token_data: Annotated[TokenData, Security(authenticated)],
    data: UserSettings,
) -> None:
    await update_user_settings(
        user_id=token_data.user_id,
        data=data,
    )
