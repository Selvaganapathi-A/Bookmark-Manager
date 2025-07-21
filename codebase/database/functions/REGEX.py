import re
from typing import Any


def regex_pattern_match(pattern: str, value: Any) -> bool:
    if value is None or not isinstance(value, str):
        return False
    if re.match(pattern, value):
        return True
    else:
        return False
