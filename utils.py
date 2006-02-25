def add_period(s):
    if not (s.endswith('.') or s.endswith('?') or s.endswith('!')):
        return s + '.'
