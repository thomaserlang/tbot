from uuid import UUID

from pydantic import BaseModel
from starlette.authentication import BaseUser

from tbot2.config_settings import config

from ..exceptions import ErrorMessage
from ..types.access_level_type import TAccessLevel
from ..types.feature_type import Feature
from ..types.scope_type import Scope


class TokenData(BaseUser, BaseModel):
    user_id: UUID
    scopes: list[str | Scope]

    @property
    def is_authenticated(self) -> bool:
        return True

    async def channel_require_access(
        self,
        *,
        channel_id: UUID,
        access_level: TAccessLevel,
        feature: Feature | None = None,
    ) -> TAccessLevel:
        from tbot2.channel_user_access import get_channel_user_access_level

        if await self.is_global_admin():
            return TAccessLevel.GLOBAL_ADMIN

        user_level = await get_channel_user_access_level(
            user_id=self.user_id,
            channel_id=channel_id,
        )
        if user_level is None or user_level.access_level < access_level.value:
            raise ErrorMessage(
                code=403,
                type='access_denied',
                message='You do not have access to this channel',
            )

        if feature:
            from tbot2.channel import get_channel

            channel = await get_channel(channel_id=channel_id)
            if not channel or feature not in channel.features:
                raise ErrorMessage(
                    code=403,
                    type='feature_access_denied',
                    message='This channel does not have access to this feature',
                )

        return user_level.access_level

    def has_any_scope(self, scopes: list[Scope]) -> bool:
        return any(scope in self.scopes for scope in scopes)

    async def is_global_admin(self) -> bool:
        return self.user_id in config.global_admins

    async def require_global_admin(self) -> None:
        if not await self.is_global_admin():
            raise ErrorMessage(
                code=403,
                type='access_denied',
                message='Access denied',
            )
