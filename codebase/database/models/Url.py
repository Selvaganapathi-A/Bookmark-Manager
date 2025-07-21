import datetime
from typing import Any, Optional

from sqlalchemy import JSON, Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ...typing_extension.URLDicts import URLDict
from .Base import Base
from .Icon import ICON


class URL(Base):
    __tablename__: str = 'URL'
    # __table_args__ = (UniqueConstraint('url', 'title', 'icon_pk', name='UniqueURLs'),)
    #
    urlAuth: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlHost: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlPort: Mapped[Optional[int]] = mapped_column(Integer,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlPath: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlQuery: Mapped[Optional[str]] = mapped_column(String,
                                                    nullable=True,
                                                    default=None,
                                                    deferred=True)
    urlFragment: Mapped[Optional[str]] = mapped_column(String,
                                                       nullable=True,
                                                       default=None,
                                                       deferred=True)
    urlScheme: Mapped[Optional[str]] = mapped_column(String,
                                                     nullable=True,
                                                     default=None,
                                                     deferred=True)
    #
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None)
    parent: Mapped[Optional[str]] = mapped_column(String,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    #
    pk: Mapped[Integer] = mapped_column(Integer,
                                        primary_key=True,
                                        autoincrement=True)
    icon_pk: Mapped[Integer] = mapped_column(Integer,
                                             ForeignKey('ICON.pk',
                                                        ondelete='SET NULL'),
                                             nullable=True)
    domain_pk: Mapped[Integer] = mapped_column(Integer,
                                               ForeignKey('DOMAIN.pk',
                                                          ondelete='CASCADE'),
                                               nullable=False)
    #
    subdomain: Mapped['SUBDOMAIN'] = relationship('SUBDOMAIN',
                                                  back_populates='urls')
    icon: Mapped['ICON'] = relationship('ICON', back_populates='urls')
    #
    note: Mapped[Optional[str]] = mapped_column(String,
                                                nullable=True,
                                                default=None,
                                                deferred=True)
    jsonnote: Mapped[dict[Any, Any]] = mapped_column(JSON,
                                                     nullable=False,
                                                     default={},
                                                     deferred=True)
    #
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        deferred=True,
    )
    modified: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, deferred=True)
    #
    tagB1: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB2: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB3: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB4: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    #
    tagN1: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN2: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN3: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN4: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    #
    tagT1: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT2: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT3: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT4: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)

    def update_url(self, new_url: str):
        self.url = new_url
        _record: URLDict = create_URLRecord(new_url)
        self.urlAuth = _record['urlAuth']
        self.urlHost = _record['urlHost']
        self.urlPort = _record['urlPort']
        self.urlPath = _record['urlPath']
        self.urlQuery = _record['urlQuery']
        self.urlFragment = _record['urlFragment']
        self.urlScheme = _record['urlScheme']
        self.modified = timestamp_provider()


class URLTemp(Base):
    __tablename__: str = 'URLTemp'
    __table_args__ = {'schema': 'temp'}
    #
    urlAuth: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlHost: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlPort: Mapped[Optional[int]] = mapped_column(Integer,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlPath: Mapped[Optional[str]] = mapped_column(String,
                                                   nullable=True,
                                                   default=None,
                                                   deferred=True)
    urlQuery: Mapped[Optional[str]] = mapped_column(String,
                                                    nullable=True,
                                                    default=None,
                                                    deferred=True)
    urlFragment: Mapped[Optional[str]] = mapped_column(String,
                                                       nullable=True,
                                                       default=None,
                                                       deferred=True)
    urlScheme: Mapped[Optional[str]] = mapped_column(String,
                                                     nullable=True,
                                                     default=None,
                                                     deferred=True)
    #
    url: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None)
    parent: Mapped[Optional[str]] = mapped_column(String,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    #
    pk: Mapped[Integer] = mapped_column(Integer,
                                        primary_key=True,
                                        autoincrement=True)
    icon_pk: Mapped[Integer] = mapped_column(Integer,
                                             ForeignKey(ICON.pk,
                                                        ondelete='SET NULL'),
                                             nullable=True)
    domain_pk: Mapped[Integer] = mapped_column(
        Integer, ForeignKey('DOMAIN.pk', ondelete='CASCADE'))
    #
    note: Mapped[Optional[str]] = mapped_column(String,
                                                nullable=True,
                                                default=None,
                                                deferred=True)
    jsonnote: Mapped[dict[Any, Any]] = mapped_column(JSON,
                                                     nullable=False,
                                                     default={},
                                                     deferred=True)
    #
    created: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        deferred=True,
    )
    modified: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None, deferred=True)
    #
    tagB1: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB2: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB3: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    tagB4: Mapped[Optional[bool]] = mapped_column(Boolean,
                                                  nullable=True,
                                                  default=None,
                                                  deferred=True)
    #
    tagN1: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN2: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN3: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagN4: Mapped[Optional[int]] = mapped_column(Integer,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    #
    tagT1: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT2: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT3: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
    tagT4: Mapped[Optional[str]] = mapped_column(String,
                                                 nullable=True,
                                                 default=None,
                                                 deferred=True)
