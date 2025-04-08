from datetime import UTC, datetime


def datetime_now():
    return datetime.now(tz=UTC)
