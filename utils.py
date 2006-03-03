terminators = '.?!'

def is_terminator(s):
    return (bool(s) and s in terminators)

def add_period(s):
    if not is_terminator(s[-1]):
        return s + '.'

def abbreviate(s):
    def parts(s):
        start = 0
        length = 0
        for letter in s:
            length += 1
            if not letter.isalpha():
                yield s[start:length], letter
                start += length
                length = 0
        yield s[start:length], ""
    def abbr(part):
        if is_terminator(part[1]):
            return part[0][0].upper() + part[1]
        else:
            return part[0][0].upper() + '.'
    return ''.join(abbr(part) for part in parts(s))

def format(s, format = "%s"):
    if s and len(s) != 0:
        return format % s
    else:
        return ""
