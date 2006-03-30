import re
from pybtex.richtext import RichText

terminators = '.?!'
dash_re = re.compile(r'-')

def set_backend(b):
    global backend
    backend = b

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
    return backend.ndash.join(dash_re.split(s))

def format(s, format = "%s"):
    if s and len(s) != 0:
        return format % s
    else:
        return ""

class Phrase:
    def __init__(self, *args, **kwargs):
        def getarg(key, default=None):
            try:
                return kwargs[key]
            except KeyError:
                return default

        self.sep = getarg('sep', ', ')
        self.last_sep = getarg('last_sep', self.sep)
        self.sep2 = getarg('sep2', self.last_sep)
        self.period = getarg('add_period', False)
        self.periods = getarg('add_periods', False)
        self.sep_after = None
        self.parts = []
        for text in args:
            self.append(text)

        self.__str__ = self.parts.__str__
        self.__repr__ = self.parts.__repr__

    def append(self, text, sep_before=None, sep_after=None):
        try:
            text = text.rich_text()
        except AttributeError:
            pass
        if text:
            if self.periods:
                text = add_period(text)

            if self.sep_after is not None:
                sep_before = self.sep_after
                self.sep_after = None
            if sep_after is not None:
                self.sep_after = sep_after

            if isinstance(text, list):
                self.parts.append((text[0], sep_before))
                for part in text[1:]:
                    self.parts.append((part, ''))
            else:
                self.parts.append((text, sep_before))

    def rich_text(self):
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            if sep:
                result.append(sep)
            result.append(part[0])

        if not self.parts:
            return RichText()
        elif len(self.parts) == 1:
            result = RichText(self.parts[0][0])
        elif len(self.parts) == 2:
            sep = self.parts[1][1]
            if sep is None:
                sep = self.sep2
            result = RichText(self.parts[0][0], sep, self.parts[1][0])
        else:
            result = RichText()
            output_part(self.parts[0], sep='')
            for part in self.parts[1:-1]:
                output_part(part, self.sep)
            output_part(self.parts[-1], self.last_sep)
        if self.period:
            result = add_period(result)
        return result

class Word(Phrase):
    def __init__(self, *args, **kwargs):
        kwargs['sep'] = ''
        kwargs['sep2'] = ''
        kwargs['last_sep'] = ''
        Phrase.__init__(self, *args, **kwargs)
