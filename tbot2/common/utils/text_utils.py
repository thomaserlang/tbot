import re
import shlex
import string

from unidecode import unidecode


def split(s: str) -> list[str]:
    if '"' not in s:
        return s.split(' ')
    try:
        return list(shlex.split(s))
    except ValueError:
        return []


def check_pattern_match(
    message: str,
    pattern: str,
    normalize: bool = False,
    strip_symbols: bool = False,
    collaps_letters: bool = False,
    check_leetspeak: bool = False,
) -> bool:
    """
    Supports regex patterns prefixed with 're:' and normal patterns.
    Single words will be matched in any poisition, words in
    quotes will be matched as a whole.

    Examples:
    - 're:[a-z ]+' will match 'hello world' or 'world hello'
    - 'hello world' will match 'hello world' and 'world hello'
    - '"hello world"' will match 'hello world' but not 'world hello'

    """
    message = message.lower()
    if normalize:
        message = normalize_message(message)
    if strip_symbols:
        message = strip_message_symbols(message)
    if collaps_letters:
        message = collaps_message_letter_repeat(message)

    if check_leetspeak:
        if _check_pattern_match(normalize_leetspeak_message(message), pattern):
            return True
    return _check_pattern_match(message, pattern)


def _check_pattern_match(message: str, pattern: str) -> bool:
    if pattern.startswith('re:'):
        if re.search(
            pattern[3:],
            message,
        ):
            return True
    else:
        words = message.split(' ')
        return all(_is_match(p, words) for p in split(pattern))
    return False


def _is_match(pattern: str, words: list[str]) -> bool:
    match_words = pattern.split(' ')
    if len(match_words) == 1:
        return match_words[0] in words
    i = 0
    try:
        while True:
            i = words.index(match_words[0], i) + 1
            k = i
            for s in match_words[1:]:
                if k >= len(words) or words[k] != s:
                    break
                k += 1
            else:
                return True
    except ValueError:
        pass
    return False


def normalize_message(message: str) -> str:
    message = unidecode(message)
    # Remove extra spaces
    message = re.sub(r'\s+', ' ', message)

    return message


_trans_leet = str.maketrans(
    {
        '4': 'a',
        '@': 'a',
        '8': 'b',
        '3': 'e',
        '9': 'g',
        '1': 'l',
        '!': 'i',
        '0': 'o',
        '5': 's',
        '$': 's',
        '7': 't',
        '2': 'z',
        '(': 'c',
        '[': 'c',
        ')': 'd',
    }
)


def normalize_leetspeak_message(message: str) -> str:
    return message.translate(_trans_leet)


def collaps_message_letter_repeat(message: str) -> str:
    return re.sub(r'(.)\1+', r'\1\1', message)


_trans_punctuation = str.maketrans('', '', string.punctuation)


def strip_message_symbols(message: str) -> str:
    return message.translate(_trans_punctuation)


def safe_username(user: str):
    return re.sub('[^a-zA-Z0-9_]', '', user)[:100]
