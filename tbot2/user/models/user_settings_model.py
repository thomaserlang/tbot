from typing import Any
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from tbot2.model_base import Base


class MUserSettings(Base):
    __tablename__ = 'user_settings'

    user_id: Mapped[UUID] = mapped_column(
        sa.UUID(as_uuid=True),
        sa.ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
    )
    settings: Mapped[dict[str, Any]] = mapped_column(
        sa.JSON(), nullable=False, default='{}'
    )
