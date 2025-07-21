import hashlib
from typing import Unpack

import models
from _typing_ import IconModelDict
from sqlalchemy import insert, select
from sqlalchemy.orm.session import Session


def __hashed_string(data: str, chunk: int = 1024):
    _hsh = hashlib.sha3_512()
    i = 0
    while True:
        tmp = data[i:i + chunk]
        if tmp == '':
            break
        _hsh.update(tmp.encode())
        i += chunk
    return _hsh.hexdigest()


def get_or_create_icon(session: Session, /, cache: dict[str, int],
                       **icon: Unpack[IconModelDict]):
    hashed_image = __hashed_string(icon['data'])
    if hashed_image in cache:
        return cache[hashed_image]
    else:
        pk: int = session.execute(
            insert(models.Icon).values(icon).returning(
                models.Icon.pk)).scalar_one()
        cache[hashed_image] = pk
    return pk


def build_iconcache(session: Session) -> dict[str, int]:
    return {
        __hashed_string(data): pk for data, pk in session.execute(
            select(models.Icon.data, models.Icon.pk)).fetchall()
    }
