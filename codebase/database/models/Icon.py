import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class ICON(Base):
    __tablename__: str = 'ICON'
    data: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_uri: Mapped[bool] = mapped_column(nullable=False, default=False)
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    domain_pk: Mapped[Integer] = mapped_column(
        Integer, ForeignKey('DOMAIN.pk', ondelete='CASCADE', deferrable=True))
    #
    domain: Mapped['DOMAIN'] = relationship('DOMAIN', back_populates='icons')
    urls: Mapped[list['URL']] = relationship('URL', back_populates='urls')
    #
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        deferred=True,
    )
    modified: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, deferred=True)
