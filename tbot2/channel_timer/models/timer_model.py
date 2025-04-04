import sys
from datetime import datetime
from typing import Literal
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.common import TProvider
from tbot2.model_base import Base

from ..schemas.timer_schemas import TimerActiveMode, TimerPickMode


class MChannelTimer(Base):
    __tablename__ = 'channel_timers'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID(), primary_key=True, default=uuid7)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID(),
        sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    messages: Mapped[list[str]] = mapped_column(sa.JSON(), nullable=False)
    interval: Mapped[int] = mapped_column(sa.SmallInteger(), nullable=False)
    enabled: Mapped[bool] = mapped_column(sa.Boolean(), nullable=False, default=True)
    next_run_at: Mapped[datetime] = mapped_column(sa.DateTime(), nullable=False)
    provider: Mapped[Literal['all'] | TProvider] = mapped_column(
        sa.String(50), nullable=False, server_default='all'
    )
    pick_mode: Mapped[TimerPickMode] = mapped_column(
        sa.String(50), nullable=False, server_default='order'
    )
    active_mode: Mapped[TimerActiveMode] = mapped_column(
        sa.String(50), nullable=False, server_default='always'
    )
    last_message_index: Mapped[int | None] = mapped_column(
        sa.SmallInteger(), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(sa.DateTime(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(sa.DateTime(), nullable=False)
