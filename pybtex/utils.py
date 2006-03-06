terminators = '.?!'

def is_terminated(s):
    try:
        return s.is_terminated()
    except AttributeError:
        return (bool(s) and s[-1] in terminators)

def add_period(s):
    if not is_terminated(s):
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

        self.sep = getarg('sep', ', ')
        self.last_sep = getarg('last_sep', self.sep)
        self.sep2 = getarg('sep2', self.last_sep)
        self.add_period = getarg('add_period', False)
        self.add_periods = getarg('add_periods', False)
        self.sep_after = None
        self.parts = []
        for text in args:
            self.append(text)

    def append(self, text, sep_before=None, sep_after=None, format=None):
        if text is not None:
            text = unicode(text)
            if text:
                if self.add_periods:
                    text = add_period(text)
                if self.sep_after is not None:
                    sep_before = self.sep_after
                    self.sep_after = None
                if sep_after is not None:
                    self.sep_after = sep_after

                if format is not None:
                    self.parts.append((format(text), sep_before, text))
                else:
                    self.parts.append((text, sep_before))

    def is_terminated(self):
        last = self.parts[-1]
        try:
            plain_text = last[2]
        except IndexError:
            plain_text = last[0]
        return (plain_text in terminators)
        
    def __unicode__(self):
        def output_part(part, sep):
            if part[1] is not None:
                sep = part[1]
            tmp.append(sep + part[0])

        if len(self.parts) == 2:
            sep = self.parts[1][1]
            if sep is None:
                sep = self.sep2
            text = self.sep2.join([part[0] for part in self.parts])
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
