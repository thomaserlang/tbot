import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.dialects.mysql import TINYINT
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import ModelBase


class MRouletteSettings(ModelBase):
    __tablename__ = 'channel_gambling_roulette_settings'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    channel_id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True)
    win_chance: Mapped[int] = mapped_column(TINYINT(unsigned=True), default=50)
    win_message: Mapped[str] = mapped_column(sa.String(250))
    lose_message: Mapped[str] = mapped_column(sa.String(250))
    allin_win_message: Mapped[str] = mapped_column(sa.String(250))
    allin_lose_message: Mapped[str] = mapped_column(sa.String(250))
    min_bet: Mapped[int] = mapped_column(sa.Integer)
    max_bet: Mapped[int] = mapped_column(sa.Integer)
