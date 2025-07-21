from typing import Optional, TypedDict


class URLDict(TypedDict):
    urlAuth: Optional[str]
    urlHost: Optional[str]
    urlPort: Optional[int]
    urlPath: Optional[str]
    urlQuery: Optional[str]
    urlFragment: Optional[str]
    urlScheme: Optional[str]


class DOMAINDict(TypedDict):
    domain: str
    subdomain: str
    urlhost: str
