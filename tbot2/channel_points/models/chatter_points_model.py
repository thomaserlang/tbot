import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MChatterPoints(ModelBase):
    __tablename__ = 'channel_chatter_points'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    chatter_id: Mapped[str] = mapped_column(sa.String(36), primary_key=True)
    provider: Mapped[str] = mapped_column(sa.String(100))
    points: Mapped[int] = mapped_column(
        INTEGER(unsigned=False), nullable=False, default=0
    )
