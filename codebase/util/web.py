from typing import Unpack
from urllib.parse import parse_qs, quote

from urllib3.util import Url, parse_url

from ..typing_extension.URLDicts import URLDict


def parts_of_url(url: str) -> URLDict:
    _tmp = parse_url(url)
    return URLDict(
        urlAuth=_tmp.auth,
        urlHost=_tmp.host,
        urlPort=_tmp.port,
        urlPath=_tmp.path,
        urlQuery=_tmp.query,
        urlFragment=_tmp.fragment,
        urlScheme=_tmp.scheme,
    )


def rebuild_url(sort_url_query: bool = False, **kwargs: Unpack[URLDict]) -> str:
    return Url(
        scheme=kwargs['urlScheme'],
        auth=kwargs['urlAuth'],
        host=kwargs['urlHost'],
        port=kwargs['urlPort'],
        path=kwargs['urlPath'],
        query=sort_query(kwargs['urlQuery'])
        if sort_url_query else kwargs['urlQuery'],
        fragment=kwargs['urlFragment'],
    ).url


def query_as_python_dict(query: str | None) -> None | dict[str, list[str]]:
    if query is None:
        return None
    return parse_qs(query)


def sort_query(query: str | None) -> None | str:
    if query is None:
        return None
    query_dict = parse_qs(query)
    return '&'.join(f'{quote(key)}={quote(value)}'
                    for key in sorted(query_dict, key=str.lower)
                    for value in sorted(query_dict[key], key=str.lower))


def remove_query_items(query: str | None,
                       items_to_remove: dict[str, list[str]]) -> None | str:
    if query is None:
        return None
    query_dict = parse_qs(query)
    for key in items_to_remove:
        if key not in query_dict:
            continue
        for value in items_to_remove[key]:
            if value in query_dict[key]:
                query_dict[key].remove(value)
    return '&'.join(f'{quote(key)}={quote(value)}' for key in query_dict
                    for value in query_dict[key])


def remove_queries(query: str | None, items_to_remove: tuple[str, ...]):
    if query is None:
        return None
    query_dict = parse_qs(query)
    for key in items_to_remove:
        if key not in query_dict:
            continue
        query_dict.pop(key)
    return '&'.join(f'{quote(key)}={quote(value)}' for key in query_dict
                    for value in query_dict[key])
