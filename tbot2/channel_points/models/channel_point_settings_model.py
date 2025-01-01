import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MChannelPointSettings(ModelBase):
    __tablename__ = 'channel_point_settings'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    enabled: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    points_name: Mapped[str] = mapped_column(sa.String(45), default='points')
    points_per_min: Mapped[int] = mapped_column(SMALLINT(unsigned=False), default=10)
    points_per_min_sub_multiplier: Mapped[int] = mapped_column(
        TINYINT(unsigned=True), default=2
    )
    points_per_sub: Mapped[int] = mapped_column(SMALLINT(unsigned=False), default=1000)
    points_per_cheer: Mapped[int] = mapped_column(SMALLINT(unsigned=False), default=2)
    ignore_users: Mapped[list[str]] = mapped_column(sa.JSON, default='[]')
