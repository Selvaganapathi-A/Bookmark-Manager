from typing import NotRequired, Optional, TypedDict


class DomainModelDict(TypedDict):
    pk: NotRequired[int | None]
    domainName: str


class IconModelDict(TypedDict):
    pk: NotRequired[int | None]
    data: str
    isUri: bool


class HostModelDict(TypedDict):
    pk: NotRequired[int | None]
    hostName: str
    subDomain: str
    hostKey: str
    domain_id: int


class UrlModelDict(TypedDict):
    pk: NotRequired[int | None]
    url: str
    title: Optional[str]
    icon_id: int | None
    host_id: int
    domain_id: int
