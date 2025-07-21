from codebase.tools import create_Record
from codebase.typing_extension import JSONParseResult


def test_create_DBRecord():
    assert create_Record.create_DBRecord(**JSONParseResult(
        url='https://username:password@host.com:80/path?query#fragment',
        title=None,
        parent='/',
        iconData=None,
        iconUri='fakeUri',
    )) == {
        'urlAuth': 'username:password',
        'urlFragment': 'fragment',
        'urlHost': 'host.com',
        'urlPath': '/path',
        'urlPort': 80,
        'urlQuery': 'query',
        'urlScheme': 'https',
        #
        'url': 'https://username:password@host.com:80/path?query#fragment',
        'title': None,
        'parent': '/',
    }
