import hashlib

COLORS = [
    '#8b58FF',
    '#8B58FF',
    '#7A7A7A',
    '#877587',
    '#B7625F',
    '#7D7E7F',
    '#837AC3',
    '#5B8969',
    '#7A7A7A',
    '#9F4EFF',
    '#8061FF',
    '#866FFF',
    '#8C68D9',
]


def username_color_generator(username: str, colors: list[str] = COLORS) -> str:
    normalized = username.lower().encode('utf-8')
    hash_digest = hashlib.md5(normalized).hexdigest()
    hash_int = int(hash_digest, 16)
    index = hash_int % len(colors)
    return colors[index]
