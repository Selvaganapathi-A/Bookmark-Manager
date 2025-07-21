import html
from pathlib import Path

import m_01_add_icon
import m_02_add_domain
import m_03_add_host
import models
from _typing_ import (DomainModelDict, HostModelDict, IconModelDict,
                      UrlModelDict)
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm.session import Session

from zurvan.codebase.tools import parse_JSON, read_data
from zurvan.codebase.typing_extension import JSONParseResult
from zurvan.codebase.util import text, web, web_domain, web_host


def handle_icon(
    session: Session,
    icon_data: str | None = None,
    icon_uri: str | None = None,
    *,
    cache: dict[str, int],
):
    if icon_data is not None and icon_uri is not None:
        m_01_add_icon.get_or_create_icon(
            session,
            cache,
            **IconModelDict(data=icon_uri, isUri=True),
        )
        return m_01_add_icon.get_or_create_icon(
            session,
            cache,
            **IconModelDict(data=icon_data, isUri=False),
        )
    elif icon_data is not None:
        if icon_data.strip() == '':
            pass
        else:
            return m_01_add_icon.get_or_create_icon(
                session,
                cache,
                **IconModelDict(data=icon_data, isUri=False),
            )
    elif icon_uri is not None:
        if icon_uri.strip() == '' or icon_uri.startswith('fake-favicon-uri:'):
            pass
        else:
            return m_01_add_icon.get_or_create_icon(
                session,
                cache,
                **IconModelDict(data=icon_uri, isUri=True),
            )
    return m_01_add_icon.get_or_create_icon(
        session,
        cache,
        **IconModelDict(data='noicon', isUri=True),
    )


def add(session: Session, cache: int = 1500):
    json_data: JSONParseResult
    records_processed: int = 0
    #
    icon_cache: dict[str, int] = m_01_add_icon.build_iconcache(session)
    domain_cache: dict[str, int] = (m_02_add_domain.build_domaincache(session))
    host_cache: dict[str, int] = m_03_add_host.build_hostcache(session)
    url_model_buffer: list[UrlModelDict] = []
    #
    for i, json_data in enumerate(
            parse_JSON.parse_urls_from_json_data(
                read_data.read_json_file(
                    read_data.walk(
                        Path(__file__).parent / "JSON"
                    ))),
            start=1,
    ):
        # * gather necessary data
        json_data['url'] = html.unescape(json_data['url'])
        # json_data['url'] = html.unescape(json_data['url'])
        json_data['title'] = text.clean(html.unescape(json_data['title'] or ''))
        #
        json_data['title'] = json_data['title'] or ''
        #
        parts_url = web.parts_of_url(json_data['url'])
        # * modifications
        if (json_data['title'].lower() == 'none' or
                json_data['title'].lower() == 'null'):
            json_data['title'] = ''
        json_data['url'] = web.rebuild_url(sort_url_query=True, **parts_url)
        # * create db instances
        # * -- * #
        icon_pk = handle_icon(
            session,
            json_data['iconData'],
            icon_uri=json_data['iconUri'],
            cache=icon_cache,
        )
        domain_model_dict: DomainModelDict = DomainModelDict(
            domainName=web_domain.domain(parts_url['urlHost']) or '# unknown')
        domain_pk = m_02_add_domain.get_or_create_domain(session,
                                                         cache=domain_cache,
                                                         **domain_model_dict)
        host_model_dict: HostModelDict = HostModelDict(
            hostName=parts_url['urlHost'] or 'unknown',
            subDomain=web_domain.sub_domain(parts_url['urlHost']) or
            '# unknown',
            hostKey=web_host.host_key(parts_url['urlHost']) or '# unknown',
            domain_id=domain_pk,
        )
        host_pk = m_03_add_host.get_or_create_host(session, host_cache,
                                                   **host_model_dict)
        #
        url_model_dict: UrlModelDict = UrlModelDict(
            url=json_data['url'],
            title=json_data['title'],
            icon_id=icon_pk,
            host_id=host_pk,
            domain_id=domain_pk,
        )
        url_model_buffer.append(url_model_dict)
        #
        if i % cache == 0:
            session.execute(
                insert(models.Url).on_conflict_do_nothing(),
                url_model_buffer,
            )
            print(i, end='\r')
            url_model_buffer.clear()
            records_processed = i

    if len(url_model_buffer) > 0:
        session.execute(
            insert(models.Url).on_conflict_do_nothing(),
            url_model_buffer,
        )
        print(records_processed + len(url_model_buffer))
        url_model_buffer.clear()
