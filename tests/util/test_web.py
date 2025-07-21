from codebase.util import web


def test_parts_of_url():
    assert web.parts_of_url(
        'http://username:password@127.0.0.1:8000/path/some+path?query=gold&query=vitamin&query=food#author'
    ) == {
        'urlAuth': 'username:password',
        'urlHost': '127.0.0.1',
        'urlPort': 8000,
        'urlPath': '/path/some+path',
        'urlQuery': 'query=gold&query=vitamin&query=food',
        'urlFragment': 'author',
        'urlScheme': 'http',
    }


def test_rebuild_url():
    assert (
        web.rebuild_url(
            **{
                'urlAuth': 'username:password',
                'urlHost': '127.0.0.1',
                'urlPort': 8000,
                'urlPath': '/path/some+path',
                'urlQuery': 'query=gold&query=vitamin&query=food',
                'urlFragment': 'author',
                'urlScheme': 'http',
            }) ==
        'http://username:password@127.0.0.1:8000/path/some+path?query=gold&query=vitamin&query=food#author'
    )


def test_query_as_python_dict():
    assert web.query_as_python_dict(None) is None
    assert web.query_as_python_dict('q=1&q=3') == {'q': ['1', '3']}


def test_sort_query():
    assert web.sort_query(None) is None
    assert web.sort_query('q=3&a=1&m=4&i=45') == 'a=1&i=45&m=4&q=3'


def test_remove_query_items():
    assert web.remove_query_items(None, {}) is None
    assert (web.remove_query_items(
        'q=3&a=1&m=4&i=45&m=876&k=565&m=72',
        {'m': ['4', '72']}) == 'q=3&a=1&m=876&i=45&k=565')
    assert (web.remove_query_items(
        'q=3&a=1&m=4&i=45&m=876&k=565&m=72',
        {
            'm': ['4', '72'],
            'op': ['8768',],
        },
    ) == 'q=3&a=1&m=876&i=45&k=565')


def test_remove_queries():
    assert web.remove_queries(None, ()) is None
    assert (web.remove_queries('q=3&a=1&m=4&i=45&m=876&k=565&m=72',
                               ('m',)) == 'q=3&a=1&i=45&k=565')
    assert (web.remove_queries('q=3&a=1&m=4&i=45&m=876&k=565&m=72',
                               ('m', 'op')) == 'q=3&a=1&i=45&k=565')
