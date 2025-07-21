import typing
from pathlib import Path

@typing.overload
def read_json_file(
    arg: Path,) -> list[typing.Any] | dict[typing.Any, typing.Any]:
    """"""


@typing.overload
def read_json_file(
    arg: typing.Generator[Path, None, None],
) -> typing.Generator[typing.Any, None, None]:
    """"""


def read_json_file(
    arg,) -> typing.Any | typing.Generator[typing.Any, None, None]:
    """"""


def walk(source: Path) -> typing.Generator[Path, None, None]:
    ...
