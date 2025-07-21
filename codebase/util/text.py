import re
from typing import Optional


def clean(
    text: Optional[str],
    *,
    regex: re.Pattern[str] = re.compile(r'^\(\d+\)\ (?P<content>.*)$'),
) -> Optional[str]:
    if text is None:
        return None
    if text == 'None':
        return None
    if (var := regex.match(text)) is not None:
        text = var.group('content')
    return None if text is None else text.strip()
