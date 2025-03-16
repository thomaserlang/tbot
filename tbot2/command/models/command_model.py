import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.model_base import Base


class MCommand(Base):
    __tablename__ = 'commands'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    cmd: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    response: Mapped[str] = mapped_column(sa.String(500), nullable=False)
    group_name: Mapped[str] = mapped_column(
        sa.String(100), nullable=False, server_default=''
    )
    global_cooldown: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    chatter_cooldown: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    mod_cooldown: Mapped[int] = mapped_column(
        sa.Integer, nullable=False, server_default='0'
    )
    enabled_status: Mapped[int] = mapped_column(
        sa.SmallInteger, nullable=False, server_default='0'
    )
    enabled: Mapped[bool] = mapped_column(
        sa.Boolean, nullable=False, server_default='1'
    )
    public: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, server_default='1')
    access_level: Mapped[int] = mapped_column(
        sa.SmallInteger, nullable=False, server_default='0'
    )
    created_at: Mapped[datetime] = mapped_column(
        sa.DateTime, nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime | None] = mapped_column(sa.DateTime, nullable=True)
