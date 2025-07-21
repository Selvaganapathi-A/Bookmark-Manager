from datetime import datetime
from typing import Any, NotRequired, Optional, TypedDict


class URLDatabaseInstanceDict(TypedDict):
    urlAuth: Optional[str]
    urlHost: Optional[str]
    urlPort: Optional[str]
    urlPath: Optional[str]
    urlQuery: Optional[str]
    urlFragment: Optional[str]
    urlScheme: Optional[str]
    #
    url: str
    title: Optional[str]
    parent: NotRequired[Optional[str]]
    #
    pk: NotRequired[int]
    icon_pk: NotRequired[Optional[int]]
    domain_pk: NotRequired[int]
    #
    note: NotRequired[Optional[str]]
    jsonnote: NotRequired[dict[Any, Any]]
    #
    created: NotRequired[datetime]
    modified: NotRequired[Optional[datetime]]
    #
    tagB1: NotRequired[Optional[bool]]
    tagB2: NotRequired[Optional[bool]]
    tagB3: NotRequired[Optional[bool]]
    tagB4: NotRequired[Optional[bool]]
    #
    tagN1: NotRequired[Optional[int]]
    tagN2: NotRequired[Optional[int]]
    tagN3: NotRequired[Optional[int]]
    tagN4: NotRequired[Optional[int]]
    #
    tagT1: NotRequired[Optional[str]]
    tagT2: NotRequired[Optional[str]]
    tagT3: NotRequired[Optional[str]]
    tagT4: NotRequired[Optional[str]]


class ICONDatabaseInstanceDict(TypedDict):
    data: str
    is_uri: bool
    pk: NotRequired[int]
    created: NotRequired[datetime]
    modified: NotRequired[Optional[datetime]]


class DOMAINDatabaseInstanceDict(TypedDict):
    domain: str
    subdomain: str
    urlhost: str
    pk: NotRequired[int]
    created: NotRequired[datetime]
    modified: NotRequired[Optional[datetime]]
