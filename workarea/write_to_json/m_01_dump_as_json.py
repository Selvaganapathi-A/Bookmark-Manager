import datetime
import pathlib
import re
from pathlib import Path
from typing import Any

import models
import orjson
from sqlalchemy import func, or_, select
from sqlalchemy.orm.session import Session


def resolve_filename_conflict(
    target: pathlib.Path,
    /,
    *,
    regex: re.Pattern[str] = re.compile(
        r'^(?P<filename>.*?)(?: (?P<timestamp>\d{4}-\d{2}-\d{2}T\d{6}\.\d{6}))?(?: \((?P<fileno>\d+)\))?$'
    ),
) -> pathlib.Path:
    if not target.exists():
        return target

    parent: pathlib.Path = target.parent
    stem: str = target.stem
    suffix: str = target.suffix
    file_no: int = 0
    use_timestamp: bool = False

    # Match existing pattern
    if (var := regex.match(stem)) is not None:
        stem = var.group('filename')
        if var.group('fileno') is not None:
            file_no = int(var.group('fileno'))
            if file_no >= 99:
                use_timestamp = True  # Switch to timestamp mode
        elif var.group('timestamp') is not None:
            use_timestamp = True  # File already has a timestamp

    new_target: pathlib.Path
    # Try file number-based approach first (up to 99)
    if not use_timestamp:
        while True:
            new_filename = (f'{stem} ({file_no:0>2d}){suffix}'
                            if file_no > 0 else f'{stem}{suffix}')
            new_target = parent / new_filename
            if not new_target.exists():
                return new_target
            file_no += 1
            if file_no > 99:  # Switch to timestamp mode
                use_timestamp = True
                break

    # Use timestamp approach
    current_timestamp = datetime.datetime.now()
    while True:
        timestamp_str = current_timestamp.strftime('%Y-%m-%dT%H%M%S.%f')
        new_target = parent / f'{stem} {timestamp_str}{suffix}'
        if not new_target.exists():
            return new_target
        current_timestamp += datetime.timedelta(milliseconds=1)


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
                bmk['iconUri'] = None if icon == 'noicon' else icon
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
    target = resolve_filename_conflict(target)

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
            if dom_urls_count + noOfUrls > 350 and len(dom_id) > 0:
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
