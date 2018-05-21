
def seconds_to_pretty(seconds):
    seconds = round(seconds)
    if seconds < 60:
        return '{} seconds'.format(seconds)

    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    ts = []
    if hours == 1:
        ts.append('1 hour')
    elif hours > 1:
        ts.append('{} hours'.format(hours))
    if minutes == 1:
        ts.append('1 min')
    elif minutes > 1:
        ts.append('{} mins'.format(minutes))

    return ' '.join(ts)