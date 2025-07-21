import typing

from ..typing_extension import JSONParseResult

@typing.overload
def parse_urls_from_json_data(
    arg: list[typing.Any],) -> typing.Generator[JSONParseResult, None, None]:
    ...


@typing.overload
def parse_urls_from_json_data(
    arg: dict[typing.Any, typing.Any],
) -> typing.Generator[JSONParseResult, None, None]:
    ...


@typing.overload
def parse_urls_from_json_data(
    arg: typing.Generator[typing.Any, None, None],
) -> typing.Generator[JSONParseResult, None, None]:
    ...


def parse_urls_from_json_data(
    arg,) -> typing.Generator[JSONParseResult, None, None]:
    ...
