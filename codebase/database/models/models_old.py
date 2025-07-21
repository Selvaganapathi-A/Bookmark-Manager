import datetime
from typing import Any, Optional

from sqlalchemy import (JSON, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, UniqueConstraint)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .Base import Base

host_icon = Table(
    'host_icon',
    Base.metadata,
    Column(
        'host_pk',
        ForeignKey('HOST.pk', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        primary_key=True,
    ),
    Column(
        'icon_pk',
        ForeignKey('ICON.pk', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
        primary_key=True,
    ),
)


class Domain(Base):
    __tablename__: str = 'DOMAIN'
    urls: Mapped['list[URL]']
    hosts: Mapped['list[Host]']


class Icon(Base):
    __tablename__: str = 'ICON'
    urls: Mapped['list[URL]']
    hosts: Mapped['list[Host]'] = relationship('HOST',
                                               back_populates='icons',
                                               secondary=host_icon)


class Host(Base):
    __tablename__: str = 'HOST'
    icon_pk: Mapped[int] = mapped_column(Integer, ForeignKey('ICON.pk'))
    icons: Mapped['list[Icon]'] = relationship('ICON',
                                               back_populates='hosts',
                                               secondary=host_icon)


class URL(Base):
    __tablename__: str = 'URL'
    __table_args__ = (
        UniqueConstraint('url', 'title', 'icon_pk', name='uniqueUrls'),
        {
            'autoload': True,
            'schema': 'temp'
        },
    )
    #
    icon_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('ICON.pk', ondelete='CASCADE', onupdate='CASCADE'),
        deferred=True,
    )
    icon: Mapped[Icon] = relationship('ICON', back_populates='urls')
    #
    host_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('HOST.pk', ondelete='CASCADE', onupdate='CASCADE'),
        deferred=True,
    )
    host: Mapped[Host] = relationship('HOST', back_populates='')
    #
    domain_pk: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('DOMAIN.pk', ondelete='CASCADE', onupdate='CASCADE'),
        deferred=True,
    )
    domain: Mapped[Domain] = relationship('DOMAIN', back_populates='domain')
