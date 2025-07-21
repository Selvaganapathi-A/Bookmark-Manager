from typing import Unpack

from ..typing_extension import (JSONParseResult, URLDatabaseInstanceDict,
                                URLDict)
from ..util import web


def _update_target(source, target):
    for key in source:
        if key in target:
            target[key] = source[key]


def create_DBRecord(**record: Unpack[JSONParseResult],
                   ) -> URLDatabaseInstanceDict:
    _url: URLDict = web.parts_of_url(record['url'])
    _db = URLDatabaseInstanceDict(
        urlAuth=None,
        urlHost=None,
        urlPort=None,
        urlPath=None,
        urlQuery=None,
        urlFragment=None,
        urlScheme=None,
        #
        url=record['url'],
        title=record['title'],
        parent=record['parent'],
    )
    _update_target(_url, _db)

    return _db
