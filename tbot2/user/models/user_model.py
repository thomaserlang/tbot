import sys
from datetime import datetime
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.model_base import Base


class MUser(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    username: Mapped[str] = mapped_column(sa.String(100), unique=True)
    email: Mapped[str | None] = mapped_column(
        sa.String(255), unique=True, nullable=True
    )
    display_name: Mapped[str] = mapped_column(sa.String(255))
    created_at: Mapped[datetime] = mapped_column(sa.DateTime)
    updated_at: Mapped[datetime | None] = mapped_column(sa.DateTime, nullable=True)
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True)
    default_channel_id: Mapped[UUID | None] = mapped_column(
        sa.UUID, sa.ForeignKey('channels.id', ondelete='set null', onupdate='cascade'), nullable=True
    )
