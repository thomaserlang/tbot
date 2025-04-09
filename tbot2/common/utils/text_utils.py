import re
import shlex


def split(s: str) -> list[str]:
    if '"' not in s:
        return s.split(' ')
    try:
        return list(shlex.split(s))
    except ValueError:
        return []


def check_pattern_match(message: str, pattern: str) -> bool:
    """
    Supports regex patterns prefixed with 're:' and normal patterns.
    Single words will be matched in any poisition, words in
    quotes will be matched as a whole.

    Examples:
    - 're:[a-z ]+' will match 'hello world' or 'world hello'
    - 'hello world' will match 'hello world' and 'world hello'
    - '"hello world"' will match 'hello world' but not 'world hello'

    """
    if pattern.startswith('re:'):
        if re.search(
            pattern[3:],
            message,
            flags=re.IGNORECASE,
        ):
            return True
    else:
        split = pattern.split(' ') if '"' not in pattern else shlex.split(pattern)
        if all(
            [
                re.search(
                    rf'\b{re.escape(s)}\b',
                    message,
                    flags=re.IGNORECASE,
                )
                for s in split
            ]
        ):
            return True
    return False


def safe_username(user: str):
    return re.sub('[^a-zA-Z0-9_]', '', user)[:100]
