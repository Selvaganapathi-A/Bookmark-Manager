from codebase.util.text import clean


def test_clean():
    assert clean('(123) Hello') == 'Hello'
    assert clean(None) is None
    assert clean('None') is None
