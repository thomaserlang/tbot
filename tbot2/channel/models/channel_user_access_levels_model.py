from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.model_base import Base


class MChannelUserAccessLevel(Base):
    __tablename__ = 'channel_user_access_levels'

    id: Mapped[UUID] = mapped_column(sa.UUID, primary_key=True, default=uuid7)
    channel_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('channels.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    user_id: Mapped[UUID] = mapped_column(
        sa.UUID,
        sa.ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'),
        nullable=False,
    )
    access_level: Mapped[int] = mapped_column(sa.SmallInteger, nullable=False)
