from typing import Optional, TypedDict


class JSONParseResult(TypedDict):
    url: str
    title: Optional[str]
    parent: Optional[str]
    iconData: Optional[str]
    iconUri: Optional[str]
