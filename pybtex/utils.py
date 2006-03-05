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

class Packer:
    def __init__(self, text=None, sep=', ', sep2=None, last_sep=None, add_period=False):
        self.parts = []
        self.append(text)
        self.sep = sep
        if last_sep is None:
            last_sep = sep
        self.last_sep = last_sep
        if sep2 is None:
            sep2 = last_sep
        self.sep2 = sep2
        self.add_period = add_period
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
