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
    '#e64980',
    '#862e9c',
    '#9c36b5',
    '#ae3ec9',
    '#d6336c',
    '#15aabf',
    '#22b8cf',
    '#12b886',
    '#0ca678',
    '#40c057',
    '#74b816',
    '#94d82d',
    '#fab005',
    '#f08c00',
]


def username_color_generator(username: str, colors: list[str] = COLORS) -> str:
    normalized = username.lower().encode('utf-8')
    hash_digest = hashlib.md5(normalized).hexdigest()
    hash_int = int(hash_digest, 16)
    index = hash_int % len(colors)
    return colors[index]
