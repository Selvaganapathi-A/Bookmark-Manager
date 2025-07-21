from codebase.tools.parse_JSON import parse_urls_from_json_data


def test_parse_urls_from_json_data():
    for x in parse_urls_from_json_data({
            'children': {
                'url':
                    'http://username:password@domain.subdomain/path/somepath/otherway?q=a&r=b&q=c&r=d&s=t&t=m&u=8&b=4',
                'title':
                    None,
            }
    }):
        assert x == {
            'iconData':
                None,
            'iconUri':
                None,
            'parent':
                '/',
            'title':
                None,
            'url':
                'http://username:password@domain.subdomain/path/somepath/otherway?q=a&r=b&q=c&r=d&s=t&t=m&u=8&b=4',
        }
