import types
import typing

from ..typing_extension.JSONParseResultDicts import \
    JSONParseResult as JSONRecord


def _process_list_items(
    data_list: list[typing.Any],
    parent: str = '/',
) -> typing.Generator[JSONRecord, None, None]:
    for data in data_list:
        yield from _parser(data=data, parent=parent)


def _process_map_items(
    data_dict: dict[typing.Any, typing.Any],
    parent: str = '/',
) -> typing.Generator[JSONRecord, None, None]:
    for key in data_dict.keys():
        yield from _parser(data=data_dict[key], parent=parent)


def __fetch_title(data: dict[typing.Any, typing.Any]) -> str | None:
    match data:
        case {'title': str() | None}:
            return data['title']
        case {'name': str() | None}:
            return data['name']
        case _:
            return None


def __fetch_iconData(data: dict[str, typing.Any]) -> str | None:
    match data:
        case {'icon_data': str() | None}:
            return data['icon_data']
        case {'iconData': str() | None}:
            return data['iconData']
        case _:
            return None


def __fetch_iconUri(data: dict[str, typing.Any]) -> str | None:
    match data:
        case {'icon_uri': str() | None}:
            return data['icon_uri']
        case {'iconUri': str() | None}:
            return data['iconUri']
        case _:
            return None


def _parser(data: typing.Any,
            parent: str = '') -> typing.Generator[JSONRecord, None, None]:
    match data:
        case {'title': str(), 'children': list()}:
            yield from _process_list_items(
                data_list=data['children'],
                parent=parent + '/' + (data['title'] or 'Unknown'),
            )
        case {'url': str()}:
            yield {
                'url': data['url'],
                'title': __fetch_title(data),
                'iconData': __fetch_iconData(data),
                'iconUri': __fetch_iconUri(data),
                'parent': parent or '/',
            }
        case {'uri': str()}:
            yield {
                'url': data['uri'],
                'title': __fetch_title(data),
                'iconData': __fetch_iconData(data),
                'iconUri': __fetch_iconUri(data),
                'parent': parent or '/',
            }
        case list():
            yield from _process_list_items(data_list=data, parent=parent)
        case dict():
            yield from _process_map_items(data_dict=data, parent=parent)
        case _:
            pass


def parse_urls_from_json_data(
    arg: typing.Union[
        list[typing.Any],
        dict[typing.Any, typing.Any],
        typing.Generator[typing.Any, None, None],
    ],
) -> typing.Generator[JSONRecord, None, None]:
    if isinstance(arg, types.GeneratorType):
        for data in arg:
            yield from _parser(data)
    elif isinstance(arg, (dict, list)):
        yield from _parser(arg)
