def fill_from_dict(message: str, data: dict[str, str | int]):
    for k in data:
        message = message.replace('{' + k + '}', str(data[k]))
    return message
