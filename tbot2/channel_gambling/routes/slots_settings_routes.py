from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Security

from tbot2.channel_points import ChannelPointSettingScope
from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.slots_settings_actions import (
    get_slots_settings,
    update_slots_settings,
)
from ..schemas.slots_settings_schema import (
    SlotsSettings,
    SlotsSettingsUpdate,
)

router = APIRouter()


@router.get(
    '/channels/{channel_id}/slots-settings',
    name='Get Slots Settings',
)
async def get_slots_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.READ])
    ],
) -> SlotsSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    settings = await get_slots_settings(
        channel_id=channel_id,
    )
    return settings


@router.put(
    '/channels/{channel_id}/slots-settings',
    name='Update Slots Settings',
)
async def update_slots_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.WRITE])
    ],
    data: SlotsSettingsUpdate,
) -> SlotsSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    settings = await update_slots_settings(
        channel_id=channel_id,
        data=data,
    )
    return settings
