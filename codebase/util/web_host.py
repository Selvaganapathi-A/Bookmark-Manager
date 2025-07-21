from .web_domain import _deal_ip_hosts


def host_key(host: str | None, _pad: int = 3) -> str | None:
    if host is None:
        return
    host = _deal_ip_hosts(host)
    if '.' in host:
        return '.'.join(f'{len(x):0>{_pad}}' for x in reversed(host.split('.')))
    else:
        return 'zero'
