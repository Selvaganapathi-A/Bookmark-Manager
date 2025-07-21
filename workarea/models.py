import datetime

from sqlalchemy import (JSON, Boolean, DateTime, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import declarative_base

Base = declarative_base()


class DOMAIN(Base):
    __tablename__ = 'DOMAIN'
    # __table_args__ = (UniqueConstraint('subdomain', name='uniqdomain'),)
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    domainName: Mapped[str] = mapped_column(String, nullable=False)
    #
    icons: Mapped[list['ICON']] = relationship('ICON', back_populates='domain')
    urls: Mapped[list['URL']] = relationship('URL', back_populates='domain')


class ICON(Base):
    __tablename__ = 'ICON'
    data: Mapped[str] = mapped_column(unique=True, nullable=False)
    is_uri: Mapped[bool] = mapped_column(nullable=False, default=False)
    #
    domain_pk: Mapped[int] = mapped_column(ForeignKey('DOMAIN.pk',
                                                      ondelete='CASCADE'),
                                           nullable=True)
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    domain: Mapped[DOMAIN] = relationship('DOMAIN', back_populates='icons')
    urls: Mapped[list['URL']] = relationship('URL', back_populates='icon')


class URL(Base):
    __tablename__ = 'URL'
    url: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=True, default=None)
    parent: Mapped[str] = mapped_column(String, nullable=True, default=None)
    #
    urlAuth: Mapped[str] = mapped_column(String,
                                         nullable=True,
                                         default=None,
                                         deferred=True)
    urlHost: Mapped[str] = mapped_column(String,
                                         nullable=True,
                                         default=None,
                                         deferred=True)
    urlPort: Mapped[int] = mapped_column(Integer,
                                         nullable=True,
                                         default=None,
                                         deferred=True)
    urlPath: Mapped[str] = mapped_column(String,
                                         nullable=True,
                                         default=None,
                                         deferred=True)
    urlQuery: Mapped[str] = mapped_column(String,
                                          nullable=True,
                                          default=None,
                                          deferred=True)
    urlFragment: Mapped[str] = mapped_column(String,
                                             nullable=True,
                                             default=None,
                                             deferred=True)
    urlScheme: Mapped[str] = mapped_column(String,
                                           nullable=True,
                                           default=None,
                                           deferred=True)
    #
    domain_pk: Mapped[int] = mapped_column(
        ForeignKey('DOMAIN.pk', ondelete='CASCADE'))
    icon_pk: Mapped[int] = mapped_column(
        ForeignKey('ICON.pk', ondelete='SET NULL'))
    #
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    icon: Mapped[ICON] = relationship('ICON', back_populates='urls')
    domain: Mapped[DOMAIN] = relationship('DOMAIN', back_populates='urls')
    #
    note: Mapped[str] = mapped_column(String,
                                      nullable=True,
                                      default=None,
                                      deferred=True)
    jsonnote: Mapped[dict] = mapped_column(JSON,
                                           nullable=False,
                                           default={},
                                           deferred=True)
    #
    created: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                       nullable=True,
                                                       default=None,
                                                       deferred=True)
    modified: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True),
                                                        nullable=True,
                                                        default=None,
                                                        deferred=True)
    #
    tagB1: Mapped[bool] = mapped_column(Boolean,
                                        nullable=True,
                                        default=None,
                                        deferred=True)
    tagB2: Mapped[bool] = mapped_column(Boolean,
                                        nullable=True,
                                        default=None,
                                        deferred=True)
    tagB3: Mapped[bool] = mapped_column(Boolean,
                                        nullable=True,
                                        default=None,
                                        deferred=True)
    tagB4: Mapped[bool] = mapped_column(Boolean,
                                        nullable=True,
                                        default=None,
                                        deferred=True)
    #
    tagN1: Mapped[int] = mapped_column(Integer,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagN2: Mapped[int] = mapped_column(Integer,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagN3: Mapped[int] = mapped_column(Integer,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagN4: Mapped[int] = mapped_column(Integer,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    #
    tagT1: Mapped[str] = mapped_column(String,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagT2: Mapped[str] = mapped_column(String,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagT3: Mapped[str] = mapped_column(String,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
    tagT4: Mapped[str] = mapped_column(String,
                                       nullable=True,
                                       default=None,
                                       deferred=True)
