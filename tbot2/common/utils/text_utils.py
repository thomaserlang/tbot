import re
import shlex


def split(s: str) -> list[str]:
    if '"' not in s:
        return s.split(' ')
    try:
        return list(shlex.split(s))
    except ValueError:
        return []


def check_message(message: str, banned_words: list[str]):
    for bw in banned_words:
        if bw.startswith('re:'):
            if re.search(bw[3:], message, flags=re.IGNORECASE):
                return True
            continue

        s = split(bw)
        if all([re.search(rf'\b{a}\b', message, flags=re.IGNORECASE) for a in s]):
            return True

    return False


def safe_username(user: str):
    return re.sub('[^a-zA-Z0-9_]', '', user)[:100]
