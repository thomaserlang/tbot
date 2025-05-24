from datetime import datetime
from typing import Any
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.common.utils.sqlalchemy_utils import UtcDateTime
from tbot2.model_base import Base


class MActivity(Base):
    __tablename__ = 'channel_activities'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    channel_id: Mapped[UUID] = mapped_column(sa.UUID, nullable=False)
    provider: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    provider_message_id: Mapped[str] = mapped_column(
        sa.String(100), nullable=False, unique=True
    )
    provider_channel_id: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    provider_viewer_id: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    viewer_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    viewer_display_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    type: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    sub_type: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    count: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    count_decimal_place: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    count_currency: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(UtcDateTime, nullable=False)
    gifted_viewers: Mapped[list[dict[str, Any]] | None] = mapped_column(
        sa.JSON, nullable=True
    )
    system_message: Mapped[str] = mapped_column(sa.String(2000))
    message: Mapped[str | None] = mapped_column(sa.String(2000), nullable=True)
    message_parts: Mapped[list[dict[str, Any]] | None] = mapped_column(
        sa.JSON, nullable=True
    )
    read: Mapped[bool] = mapped_column(sa.Boolean, default=False, nullable=False)
