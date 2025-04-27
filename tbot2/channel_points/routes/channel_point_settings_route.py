from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Security

from tbot2.common import TAccessLevel, TokenData
from tbot2.dependecies import authenticated

from ..actions.channel_point_settings_actions import (
    get_channel_point_settings,
    update_channel_point_settings,
)
from ..schemas.channel_point_settings_schema import (
    ChannelPointSettings,
    ChannelPointSettingsUpdate,
)
from ..types import ChannelPointSettingScope

router = APIRouter()


@router.get(
    '/channels/{channel_id}/point-settings',
    name='Get Channel Point Settings',
)
async def get_channel_point_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.READ])
    ],
) -> ChannelPointSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    channel_point_settings = await get_channel_point_settings(
        channel_id=channel_id,
    )
    return channel_point_settings


@router.put(
    '/channels/{channel_id}/point-settings',
    name='Update Channel Point Settings',
)
async def update_channel_point_settings_route(
    channel_id: UUID,
    token_data: Annotated[
        TokenData, Security(authenticated, scopes=[ChannelPointSettingScope.WRITE])
    ],
    data: ChannelPointSettingsUpdate,
) -> ChannelPointSettings:
    await token_data.channel_require_access(
        channel_id=channel_id,
        access_level=TAccessLevel.MOD,
    )

    channel_point_settings = await update_channel_point_settings(
        channel_id=channel_id,
        data=data,
    )
    return channel_point_settings
