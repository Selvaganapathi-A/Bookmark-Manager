from codebase.util import web_domain


def test_sub_domain():
    assert web_domain.sub_domain(None) is None
    #
    urlHost = r'127.0.0.1'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-internal'

    urlHost = r'192.168.159.37'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-local'

    urlHost = r'localhost'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-internal'

    urlHost = r'www.google.com'
    assert web_domain.sub_domain(urlHost) == 'com.google.www'

    urlHost = r'101.1.10.22'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-www'

    urlHost = r'1.1.1.1'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-www'

    urlHost = r'102.1.71.83'
    assert web_domain.sub_domain(urlHost) == '$$$ ip-www'

    urlHost = r'992.1.71.83'
    assert web_domain.sub_domain(urlHost) == '83.71.1.992'

    urlHost = r'www.google.co.in'
    assert web_domain.sub_domain(urlHost) == 'in.co.google.www'

    urlHost = r'www.google.co.in'
    assert web_domain.sub_domain(urlHost) == 'in.co.google.www'

    urlHost = r'tngia.gov.co.in'
    assert web_domain.sub_domain(urlHost) == 'in.co.gov.tngia'


def test_getDomain():
    assert web_domain.domain(None) is None
    assert web_domain.domain('www.google.co.in') == 'in.co.google'
    assert web_domain.domain('video.alphabet.co') == 'co.alphabet'
    assert web_domain.domain('www.css.cafe') == 'cafe.css'
