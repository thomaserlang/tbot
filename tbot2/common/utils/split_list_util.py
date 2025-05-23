def split_list(data: list[str] | None) -> list[str]:
    """Split a list of comma separated strings and return a list of strings."""
    if not data:
        return []
    result: list[str] = []
    for d in data:
        if d:
            result.extend(d.split(','))
    return [e.strip() for e in result]
