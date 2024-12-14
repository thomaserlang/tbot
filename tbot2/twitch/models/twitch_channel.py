import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MTwitchChannel(ModelBase):
    __tablename__ = 'twitch_channels'

    channel_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(25))
    twitch_token: Mapped[str] = mapped_column(sa.String(200))
    twitch_refresh_token: Mapped[str] = mapped_column(sa.String(200))
    twitch_scope: Mapped[list[str]] = mapped_column(sa.JSON)
