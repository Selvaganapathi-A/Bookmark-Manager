from pathlib import Path
from typing import Any

import orjson
from automate.m_util_functions import functions_path
from models import Domain, Host, Icon, Url
from sqlalchemy import func, or_, select
from sqlalchemy.orm.session import Session


def write(data: dict[str, Any], index: int = 1):
    target = Path(__file__).parent / 'JSON' / 'bookmark (01).json'
    target = functions_path.resolve_filename_conflict(target)
    with target.open('wb') as writer:
        writer.write(orjson.dumps(data))
        writer.flush()
        writer.close()
    print(target)


def write_to_file(
    session: Session,
    *domain_ids: int,
    fetch_limit: int = 100,
    urls_per_file: int = 2000,
):
    urls_written: int = 0
    offset: int = 0
    file_index: int = 1
    collection_of_bookmark: dict[str, Any] = {
        'title': 'Bookmarks Folder',
        'children': [],
    }
    #
    query = (select(
        Url.url,
        Url.title,
        Icon.data,
        Icon.isUri,
        Host.subDomain,
        Domain.domainName,
    ).filter(or_(*(Domain.pk == domain_id for domain_id in domain_ids))).join(
        Domain,
        Url.domain_id == Domain.pk).join(Host, Url.host_id == Host.pk).join(
            Icon, Url.icon_id == Icon.pk).order_by(
                Domain.domainName.asc().nulls_last(),
                Host.subDomain.asc().nulls_last(),
                Url.url.asc().nulls_last(),
                Url.title.asc().nulls_last(),
                Icon.isUri,
            ))

    result = session.execute(query.slice(offset,
                                         stop=offset + fetch_limit)).all()
    while len(result) > 0:
        for url, title, icon, isUri, subdomain, domain in result:
            bookmark = {}
            bookmark['title'] = title or None
            bookmark['url'] = url
            if isUri:
                if icon == 'noicon':
                    bookmark['iconData'] = None
                else:
                    bookmark['iconUri'] = icon
            else:
                bookmark['iconData'] = icon
            collection_of_bookmark['children'].append(bookmark)
            # pprint((url, title, isUri, subdomain, domain))
            # pprint(bookmark, sort_dicts=False)
            urls_written += 1
            if urls_written >= urls_per_file:
                write(collection_of_bookmark, file_index)
                urls_written = 0
                collection_of_bookmark.clear()
                collection_of_bookmark['title'] = (
                    'Bookmarks from Python Data Dump')
                collection_of_bookmark['children'] = []
                file_index += 1

        offset += fetch_limit
        result = session.execute(query.slice(offset,
                                             offset + fetch_limit)).all()

    if urls_written > 0:
        write(collection_of_bookmark)
        urls_written = 0
        collection_of_bookmark.clear()


def dump(session: Session, fetch_limit: int = 50):
    bookmarks_per_file: int = 2000
    offset: int = 0
    urls_written = 0
    #
    ds = (select(
        func.count(Url.pk).label('noOfUrls'),
        Url.domain_id,
    ).group_by(Url.domain_id).subquery())
    # * bulk domain writes
    offset = 0
    #
    domain_select_query = (select(ds.c.noOfUrls, ds.c.domain_id).join(
        Domain, ds.c.domain_id == Domain.pk).order_by(ds.c.noOfUrls.desc(),
                                                      Domain.domainName))
    #
    result = session.execute(
        domain_select_query.slice(offset, offset + fetch_limit)).all()
    #
    dom_id: list[int] = []
    dom_urls_count: int = 0
    #
    while len(result) > 0:
        for noOfUrls, domain_id in result:
            if (dom_urls_count + noOfUrls > bookmarks_per_file and
                    len(dom_id) > 0):
                write_to_file(
                    session,
                    *dom_id,
                    urls_per_file=bookmarks_per_file,
                )
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
        write_to_file(session, *dom_id, urls_per_file=bookmarks_per_file)

    print(urls_written)
