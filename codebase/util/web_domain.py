import re
from functools import lru_cache

octate: str = r'((25[0-5])|(2[0-4][0-9])|(1\d{2})|([1-9]?\d))'

IP_ADDRESS_GLOBAL: re.Pattern[str] = re.compile(
    (rf'^{octate}\.{octate}\.{octate}\.{octate}'))

IP_ADDRESS_INTERNAL: re.Pattern[str] = re.compile(
    (rf'^127\.{octate}\.{octate}\.{octate}'))

IP_ADDRESS_LOCAL_AREA_NETWORK: re.Pattern[str] = re.compile(
    (rf'^192\.{octate}\.{octate}\.{octate}'))


@lru_cache(512)
def _deal_ip_hosts(host: str) -> str:
    if host.lower() == 'localhost':
        return '$$$ ip-internal'
    elif len(host) < 7:
        return host
    elif 15 < len(host):
        return host
    else:
        global IP_ADDRESS_GLOBAL, IP_ADDRESS_INTERNAL, IP_ADDRESS_LOCAL_AREA_NETWORK
        if IP_ADDRESS_LOCAL_AREA_NETWORK.match(host):
            return '$$$ ip-local'
        elif IP_ADDRESS_INTERNAL.match(host):
            return '$$$ ip-internal'
        elif IP_ADDRESS_GLOBAL.match(host):
            return '$$$ ip-www'
        else:
            return host


def sub_domain(host: str | None) -> str | None:
    if host is None:
        return
    host = _deal_ip_hosts(host)
    return '.'.join(reversed(host.split('.')))


def domain(host: str | None) -> str | None:
    if host is None:
        return
    host = _deal_ip_hosts(host)
    _dom = []
    dom = host.split('.')
    if dom[0] in (
            'www0',
            'www1',
            'www2',
            'www3',
            'www4',
            'www5',
            'www6',
            'www7',
            'www8',
            'www9',
            'm',
            'www',
    ):
        dom.pop(0)
    word_length: int = 0
    for word in reversed(dom):
        if word_length >= 6:
            break
        word_length += len(word)
        _dom.append(word)
    return '.'.join(_dom)
