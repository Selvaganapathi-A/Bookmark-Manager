import html
from pathlib import Path
from typing import Any

import orjson
from m_01_dump_as_json import resolve_filename_conflict
from models import Domain, Host, Icon, Url
from sqlalchemy import func, or_, select
from sqlalchemy.orm.session import Session


def write_icons_to_file(session: Session, fetch_limit: int = 100):
    offset: int = 0
    query = select(
        Icon.data,
        Icon.pk,
        Icon.isUri,
    ).order_by(Icon.isUri, Icon.pk)
    #
    # <img src="" alt="" srcset="">
    #
    result = session.execute(query.slice(offset, offset + fetch_limit)).all()
    parent = Path(__file__).parent / 'JSON'
    file = parent / r'index.html'
    fd = file.open('w')
    while len(result) > 0:
        for icon, pk, wasUri in result:
            if wasUri:
                fd.write('<div class= "no-icon" >')
                fd.write(f'<span>{pk}</span>')
                fd.write(f'<p>{icon}</p>')
                fd.write('</div>')
                fd.write('\n')
            else:
                fd.write('<div class= "icon" >')
                fd.write(f'<span>{pk}</span>')
                fd.write(f'<img src="{icon}" alt="icon" >')
                fd.write('</div>')
                fd.write('\n')

        offset += fetch_limit
        result = session.execute(query.slice(offset, offset + fetch_limit)).all()
    fd.flush()
    fd.close()
