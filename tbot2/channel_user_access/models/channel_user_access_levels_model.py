import sys
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from tbot2.common import TAccessLevel
from tbot2.model_base import Base
from tbot2.user import MUser


class MChannelUserAccessLevel(Base):
    __tablename__ = 'channel_user_access_levels'
    __table_args__ = {'extend_existing': 'pytest' in sys.modules}

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
    access_level: Mapped[TAccessLevel] = mapped_column(sa.SmallInteger, nullable=False)


class MChannelUserAccessLevelWithUser(MChannelUserAccessLevel):
    user: Mapped[MUser] = sa.orm.relationship(MUser, lazy='joined', innerjoin=True)
