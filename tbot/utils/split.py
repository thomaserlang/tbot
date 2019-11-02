import shlex

def split(s):
    if '"' not in s:
        return s.split(' ')
    try:
        return list(shlex.split(s))
    except ValueError:
        pass