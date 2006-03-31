import re
from pybtex.richtext import RichText, Symbol, Phrase

terminators = '.?!'
dash_re = re.compile(r'-')

def is_terminated(s):
    try:
        return s.is_terminated()
    except AttributeError:
        return (bool(s) and s[-1] in terminators)

def add_period(s):
    try:
        return s.add_period()
    except AttributeError:
        try:
            s = s.rich_text()
        except AttributeError:
            pass
        if s and not is_terminated(s):
            s += '.'
        return s

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
        if is_terminated(part[1]):
            return part[0][0].upper() + part[1]
        else:
            return part[0][0].upper() + '.'
    return ''.join(abbr(part) for part in parts(s))

def dashify(s):
    return Phrase(dash_re.split(s), sep=Symbol('ndash')).rich_text()

def try_format(s, format = "%s"):
    if s:
        tmp = format.split('%s')
        tmp.insert(1, s)
        return RichText(*tmp)
    else:
        return ""
