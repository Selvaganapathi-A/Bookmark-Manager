from typing import Unpack

import models
from _typing_ import DomainModelDict
from sqlalchemy import insert, select
from sqlalchemy.orm.session import Session


def get_or_create_domain(session: Session, /, cache: dict[str, int],
                         **domain: Unpack[DomainModelDict]):
    if domain['domainName'] in cache:
        return cache[domain['domainName']]
    else:
        pk: int = session.execute(
            insert(models.Domain).values(domain).returning(
                models.Domain.pk)).scalar_one()
        cache[domain['domainName']] = pk
    return pk


def build_domaincache(session: Session) -> dict[str, int]:
    return {  # noqa: C416
        domainName: pk for domainName, pk in session.execute(
            select(models.Domain.domainName, models.Domain.pk)).fetchall()
    }
