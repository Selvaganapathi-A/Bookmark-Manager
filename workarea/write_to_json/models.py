from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class Icon(Base):
    __tablename__: str = 'Icon'
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    data: Mapped[str] = mapped_column(String(collation='binary'),
                                      nullable=False,
                                      deferred=True)
    isUri: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    tag: Mapped[int] = mapped_column(Integer,
                                     nullable=True,
                                     deferred=True,
                                     doc='NotRequired')
    #
    urls: Mapped['list[Url]'] = relationship('Url', back_populates='icon')


class Domain(Base):
    __tablename__: str = 'Domain'
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    domainName: Mapped[str] = mapped_column(String(length=1024),
                                            nullable=False,
                                            deferred=True)
    tag: Mapped[int] = mapped_column(Integer,
                                     nullable=True,
                                     deferred=True,
                                     doc='NotRequired')
    #
    urls: Mapped['list[Url]'] = relationship('Url', back_populates='domain')
    hosts: Mapped['list[Host]'] = relationship('Host', back_populates='domain')


class Host(Base):
    __tablename__: str = 'Host'
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    hostKey: Mapped[str] = mapped_column(String(length=128),
                                         nullable=False,
                                         deferred=True)
    hostName: Mapped[str] = mapped_column(String(length=1024),
                                          nullable=False,
                                          deferred=True)
    subDomain: Mapped[str] = mapped_column(String(length=1024),
                                           nullable=False,
                                           deferred=True)
    tag: Mapped[int] = mapped_column(Integer,
                                     nullable=True,
                                     deferred=True,
                                     doc='NotRequired')
    #
    domain_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('Domain.pk', ondelete='CASCADE'),
        nullable=False,
        deferred=True,
    )
    domain: Mapped['Domain'] = relationship('Domain', back_populates='hosts')
    #
    urls: Mapped['list[Url]'] = relationship('Url', back_populates='host')


class Url(Base):
    __tablename__: str = 'Url'
    __table_args__ = (UniqueConstraint('url',
                                       'title',
                                       'icon_id',
                                       name='uniqueUrls'),)
    pk: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    #
    url: Mapped[str] = mapped_column(String, nullable=False, deferred=True)
    title: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=False,
                                                 deferred=True)
    tag: Mapped[int] = mapped_column(Integer,
                                     nullable=True,
                                     deferred=True,
                                     doc='NotRequired')
    #
    icon_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('Icon.pk', ondelete='SET NULL'),
        nullable=False,
        deferred=True,
    )
    icon: Mapped['Icon'] = relationship('Icon', back_populates='urls')
    #
    host_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('Host.pk', ondelete='CASCADE'),
        nullable=False,
        deferred=True,
    )
    host: Mapped['Host'] = relationship('Host', back_populates='urls')
    #
    domain_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('Domain.pk', ondelete='CASCADE'),
        nullable=False,
        deferred=True,
    )
    domain: Mapped['Domain'] = relationship('Domain', back_populates='urls')
