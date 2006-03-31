import utils

class RichText(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self)
        for i in args:
            self.append(i)
    def append(self, item):
        if item:
            list.append(self, item)
    def render(self, backend):
        text = []
        for item in self:
            try:
                text.append(item.render(backend))
            except AttributeError:
                text.append(item)
        return "".join(text)
    def is_terminated(self):
        try:
            item = self[-1]
        except IndexError:
            return False
        try:
            return item.is_terminated()
        except AttributeError:
            return utils.is_terminated(item)
    def add_period(self):
        if not self.is_terminated():
            self.append('.')
        return self


class Tag:
    def __init__(self, name, text):
        self.name = name
        self.text = text
    def is_terminated(self):
        return utils.is_terminated(self.text)
    def render(self, backend):
        try:
            text = self.text.render(backend)
        except AttributeError:
            text = self.text
        return backend.format_tag(self.name, text)
    def add_period(self):
        return RichText(self).add_period()


class Symbol:
    def __init__(self, name):
        self.name = name
    def render(self, backend):
        return backend.symbols[self.name]


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
            if isinstance(text, list):
                for i in text:
                    self.append(i)
            else:
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
                text = utils.add_period(text)

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
            result.add_period()
        return result


def main():
    t = RichText('This is a ', Tag('emph', 'very'), ' rich text.')
    t.append(' Another sentense. ')
    t.append(RichText(' Another text. ', Tag('textbf', 'Some bold text.')))
    print t
    print t.render(None) 
    print t.is_terminated()

if __name__ == '__main__':
    main()
