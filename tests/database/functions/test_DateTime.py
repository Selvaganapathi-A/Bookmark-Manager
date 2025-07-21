from codebase.database.functions.DateTime import between


def test_between():
    from datetime import datetime

    assert (between(
        datetime(1994, 1, 1),
        datetime(1996, 1, 1),
        datetime(1995, 12, 25),
    ) is True)
    assert (between(
        datetime(1994, 1, 1),
        datetime(1996, 1, 1),
        'Jan 22',
    ) is False)
