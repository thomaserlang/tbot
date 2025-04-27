from uuid import UUID

import orjson


def _default(obj: object) -> str:
    if isinstance(obj, UUID):
        return str(obj)
    raise TypeError


def json_dumps(
    obj: object,
) -> str:
    return orjson.dumps(obj, default=_default, option=orjson.OPT_NAIVE_UTC).decode(
        'utf-8'
    )
