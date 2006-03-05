terminators = '.?!'

def is_terminator(s):
    return (bool(s) and s in terminators)

def add_period(s):
    if not is_terminator(s[-1]):
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

class Pack:
    def __init__(self, *args, **kwargs):
        def getarg(key, default=None):
            try:
                return kwargs[key]
            except KeyError:
                return default

        self.parts = []
        for text in args:
            self.append(text)
        self.sep = getarg('sep', ', ')
        self.last_sep = getarg('last_sep', self.sep)
        self.sep2 = getarg('sep2', self.last_sep)
        self.add_period = getarg(add_period, False)
        self.sep_after = None

    def append(self, text, sep_before=None, sep_after=None):
        if text is not None:
            text = str(text)
            if self.sep_after is not None:
                sep_before = self.sep_after
                self.sep_after = None
            if sep_after is not None:
                self.sep_after = sep_after
            if text:
                self.parts.append((text, sep_before))

    def __str__(self):
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            tmp.append(sep + part[0])

        if len(self.parts) == 2:
            text = self.sep2.join(self.parts)
        else:
            tmp = []
            output_part(self.parts[0], sep='')
            for part in self.parts[1:-1]:
                output_part(part, self.sep)
            output_part(self.parts[-1], self.last_sep)
            text = ''.join(tmp)
        if self.add_period:
            text = add_period(text)
        return text
