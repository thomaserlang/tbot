import shlex, re
from typing import List

def split(s):
    if '"' not in s:
        return s.split(' ')
    try:
        return list(shlex.split(s))
    except ValueError:
        pass

def check_message(message: str, banned_words: List[str]):
    for bw in banned_words:
        if bw.startswith('re:'):
            if re.search(bw[3:], message, flags=re.IGNORECASE):
                return True
            continue

        s = split(bw)
        if all([re.search(rf'\b{a}\b', message, flags=re.IGNORECASE) for a in s]):
            return True
            
    return False