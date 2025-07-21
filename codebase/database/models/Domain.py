import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base


class DOMAIN(Base):
    __tablename__: str = 'DOMAIN'
    #
    domainName: Mapped[str] = mapped_column(String,
                                            nullable=True,
                                            default=None,
                                            deferred=True)
    #
    pk: Mapped[Integer] = mapped_column(Integer,
                                        primary_key=True,
                                        autoincrement=True)
    #
    subdomains: Mapped['list[SUBDOMAIN]'] = relationship(
        'SUBDOMAIN', back_populates='domain')
    icons: Mapped['list[ICON]'] = relationship('ICON', back_populates='domain')
    #
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=func.now(),
        deferred=True,
    )
    modified: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, deferred=True)


class SUBDOMAIN(Base):
    __tablename__: str = 'SUBDOMAIN'
    #
    subdomainAddress: Mapped[str] = mapped_column(String,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    #
    pk: Mapped[Integer] = mapped_column(Integer,
                                        primary_key=True,
                                        autoincrement=True)
    domain_pk: Mapped[Integer] = mapped_column(
        Integer, ForeignKey('DOMAIN.pk', ondelete='CASCADE', deferrable=True))
    #
    domain: Mapped[DOMAIN] = relationship(  # type: ignore  # noqa: F821
        'DOMAIN', back_populates='subdomains')
    #
    domain: Mapped['DOMAIN'] = relationship('DOMAIN',
                                            back_populates='subdomains')
    urls: Mapped[list['URL']] = relationship('URL', back_populates='urls')
    #
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        deferred=True,
    )
    modified: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, deferred=True)
