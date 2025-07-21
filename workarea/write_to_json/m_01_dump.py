import sys
from pathlib import Path
from pprint import pprint
from typing import Any, Iterable

import models
import orjson
from automate.m_util_functions import functions_path
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm.session import Session


def read_urls(
    session: Session,
    host_id: int,
    urlsList: list[dict[str, Any]],
    fetch_limit: int = 50,
):
    offset: int = 0
    query = (select(
        models.Url.url,
        models.Url.title,
        models.Icon.isUri,
        models.Icon.data,
    ).filter(models.Url.host_id == host_id).join(
        models.Icon, models.Url.icon_id == models.Icon.pk)).order_by(
            models.Url.url.asc(),
            models.Url.title.asc(),
            models.Icon.isUri.desc(),
        )
    result = session.execute(query.slice(offset, offset + fetch_limit)).all()
    while len(result) > 0:
        for url, title, isUri, icon in result:
            bmk = {}
            bmk['url'] = url
            bmk['title'] = title or None
            if isUri:
                bmk['iconUri'] = (None if icon == 'noicon' else icon)
            else:
                bmk['iconData'] = icon
            urlsList.append(bmk)
        offset += fetch_limit
        result = session.execute(query.slice(offset,
                                             offset + fetch_limit)).all()


def read_subdomain(
    session: Session,
    *host_ids: int,
    subdomainList: list[dict[str, Any]],
    fetch_limit: int = 50,
):
    offset: int = 0
    query = select(models.Host.subDomain, models.Host.pk).filter(
        or_(*(models.Host.pk == host_id for host_id in host_ids)))
    result = session.execute(query.slice(offset, offset + fetch_limit)).all()
    while len(result) > 0:
        for subdomain, pk in result:
            bmk = {}
            bmk['title'] = subdomain
            bmk['children'] = []
            read_urls(session, pk, bmk['children'])
            subdomainList.append(bmk)
        offset += fetch_limit
        result = session.execute(query.slice(offset,
                                             offset + fetch_limit)).all()


def read_domain(
    session: Session,
    *domain_ids: int,
    fetch_limit: int = 50,
):
    offset: int = 0
    bookmark_file: dict[str, Any] = {
        'title': 'Bookmarks Folder',
        'children': [],
    }
    data_to_write: list[dict[str, Any]] = bookmark_file['children']

    #
    query = select(models.Domain.domainName, models.Domain.pk).filter(
        or_(*(models.Domain.pk == domain_id for domain_id in domain_ids)))

    result = session.execute(query.slice(offset, offset + fetch_limit)).all()
    while len(result) > 0:
        for domain, pk in result:
            bookmark_info: dict[str, Any] = {}
            bookmark_info['title'] = domain
            bookmark_info['children'] = []
            data_to_write.append(bookmark_info)
            read_subdomain(
                session,
                *(session.execute(
                    select(models.Host.pk).filter(
                        models.Host.domain_id == pk)).scalars().all()),
                subdomainList=bookmark_info['children'],
            )
        offset += fetch_limit
        result = session.execute(query.slice(offset,
                                             offset + fetch_limit)).all()

    target = Path(__file__).parent / 'JSON' / 'bmk.json'
    target = functions_path.resolve_filename_conflict(target)

    with target.open('wb') as writer:
        writer.write(orjson.dumps(bookmark_file))
        writer.flush()
        writer.close()


def dump(session: Session, fetch_limit: int = 50):
    offset: int = 0
    urls_written = 0
    #
    ds = (select(
        func.count(models.Url.pk).label('noOfUrls'),
        models.Url.domain_id,
    ).group_by(models.Url.domain_id).subquery())
    # * bulk domain writes
    offset = 0
    #
    domain_select_query = (select(ds.c.noOfUrls, ds.c.domain_id).join(
        models.Domain,
        ds.c.domain_id == models.Domain.pk).order_by(ds.c.noOfUrls.desc(),
                                                     models.Domain.domainName))
    #
    result = session.execute(
        domain_select_query.slice(offset, offset + fetch_limit)).all()
    #
    dom_id: list[int] = []
    dom_urls_count: int = 0
    while len(result) > 0:
        for noOfUrls, domain_id in result:
            if (dom_urls_count + noOfUrls > 350 and len(dom_id) > 0):
                read_domain(session, *dom_id)
                urls_written += dom_urls_count
                print(dom_urls_count)
                dom_id.clear()
                dom_urls_count = 0
            dom_id.append(domain_id)
            dom_urls_count += noOfUrls
        offset += fetch_limit
        result = session.execute(
            domain_select_query.slice(offset, offset + fetch_limit)).all()

    if dom_urls_count > 0:
        print(dom_urls_count)
        urls_written += dom_urls_count
        read_domain(session, *dom_id)

    print(urls_written)
