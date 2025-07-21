from datetime import datetime
from typing import Any

def between(past: datetime, future: datetime, value: Any) -> bool:
    """Check if the given date is between the two dates(past, future)

    `between(datetime(1994,1,1), datetime(2024,12,31), datetime(2010,1,1))`
    return `True`
    """
