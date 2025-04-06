import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.common import TAccessLevel
from tbot2.model_base import Base


class MChatFilter(Base):
    __tablename__ = 'chat_filters'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    provider: Mapped[str] = mapped_column(sa.String(50), nullable=False)
    name: Mapped[str] = mapped_column(sa.String(500), nullable=False)
    enabled: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
    exclude_access_level: Mapped[TAccessLevel] = mapped_column(
        sa.Integer, nullable=False
    )
    warning_enabled: Mapped[bool] = mapped_column(sa.Boolean, nullable=False)
    warning_message: Mapped[str] = mapped_column(sa.String(1000), nullable=False)
    warning_expire_duration: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    timeout_message: Mapped[str] = mapped_column(sa.String(1000), nullable=False)
    timeout_duration: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    settings: Mapped[dict[str, str | int]] = mapped_column(sa.JSON(), nullable=True)
