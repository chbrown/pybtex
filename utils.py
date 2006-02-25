def add_period(s):
    if not (s.endswith('.') or s.endswith('?') or s.endswith('!')):
        return s + '.'

def abbreviate(s):
    return add_period(s[0].upper())
