from datetime import datetime
from typing import Any


def between(past: datetime, future: datetime, value: Any) -> bool:
    assert isinstance(future, datetime)
    assert isinstance(past, datetime)
    if value is None or not isinstance(value, datetime):
        return False
    return past <= value <= future
