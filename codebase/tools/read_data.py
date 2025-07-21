import typing
from functools import singledispatch
from pathlib import Path

import orjson


def walk(source: Path) -> typing.Generator[Path, typing.Any, None]:
    for root, dirs, files in source.walk(top_down=True):
        for filename in filter(lambda file: file.lower().endswith('json'),
                               files):
            filepath: Path = root / filename
            yield filepath


def _read(path: Path) -> typing.Any:
    data = None
    with path.open('rb') as reader:
        data = orjson.loads(reader.read())
        reader.close()
    return data


@singledispatch
def read_json_file(
    arg: typing.Generator[Path, None, None],
) -> typing.Any | typing.Generator[typing.Any, None, None]:
    for file in arg:
        yield _read(file)


@read_json_file.register
def _(arg: Path) -> typing.Any | typing.Generator[typing.Any, None, None]:
    return _read(arg)
