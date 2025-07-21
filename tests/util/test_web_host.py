from codebase.util import web_host


def test_host_key():
    assert web_host.host_key(None) is None
    #
    urlHost = r'127.0.0.1'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'192.168.159.37'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'localhost'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'www.google.com'
    assert web_host.host_key(urlHost) == '003.006.003'

    urlHost = r'101.1.10.22'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'1.1.1.1'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'102.1.71.83'
    assert web_host.host_key(urlHost) == 'zero'

    urlHost = r'bing.co.in'
    assert web_host.host_key(urlHost) == '002.002.004'

    urlHost = r'www.google.co.in'
    assert web_host.host_key(urlHost) == '002.002.006.003'

    urlHost = r'tngia.gov.co.in'
    assert web_host.host_key(urlHost) == '002.002.003.005'

    urlHost = r't.me'
    assert web_host.host_key(urlHost) == '002.001'
