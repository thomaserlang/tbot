from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.model_base import Base


class MChatFilterBannedTerms(Base):
    __tablename__ = 'chat_filter_banned_terms'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    chat_filter_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('chat_filters.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(sa.String(1000), nullable=False)
    enabled: Mapped[bool] = mapped_column(sa.Boolean, nullable=False, default=True)
