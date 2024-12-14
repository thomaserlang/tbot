from datetime import datetime, timezone


def datetime_now():
    return datetime.now(tz=timezone.utc)
