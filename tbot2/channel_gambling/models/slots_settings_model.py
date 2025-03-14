import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MSlotsSettings(Base):
    __tablename__ = 'channel_gambling_slots_settings'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    emotes: Mapped[list[str]] = mapped_column(sa.JSON, nullable=False, default='[]')
    emote_pool_size: Mapped[int] = mapped_column(
        TINYINT(unsigned=True), nullable=False, default=3
    )
    payout_percent: Mapped[int] = mapped_column(
        TINYINT(unsigned=True), nullable=False, default=100
    )
    win_message: Mapped[str | None] = mapped_column(sa.String(250))
    lose_message: Mapped[str | None] = mapped_column(sa.String(250))
    allin_win_message: Mapped[str | None] = mapped_column(sa.String(250))
    allin_lose_message: Mapped[str | None] = mapped_column(sa.String(250))
    min_bet: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=5)
    max_bet: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
