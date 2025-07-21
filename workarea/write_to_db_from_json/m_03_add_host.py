from typing import Unpack

import models
from _typing_ import HostModelDict
from sqlalchemy import insert, select
from sqlalchemy.orm.session import Session


def get_or_create_host(session: Session, /, cache: dict[str, int],
                       **host: Unpack[HostModelDict]):
    if host['hostName'] in cache:
        return cache[host['hostName']]
    else:
        pk: int = session.execute(
            insert(models.Host).values(host).returning(
                models.Host.pk)).scalar_one()
        cache[host['hostName']] = pk
    return pk


def build_hostcache(session: Session) -> dict[str, int]:
    return {  # noqa : C416
        domainName: pk for domainName, pk in session.execute(
            select(models.Domain.domainName, models.Domain.pk)).fetchall()
    }
