import utils

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


class Symbol:
    def __init__(self, name):
        self.name = name
    def render(self, backend):
        return backend.symbols[self.name]


class RichText(list):
    def __init__(self, *args, **kwargs):
        list.__init__(self)
        for i in args:
            self.append(i)
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


def main():
    t = RichText('This is a ', Tag('emph', 'very'), ' rich text.')
    t.append(' Another sentense. ')
    t.append(RichText(' Another text. ', Tag('textbf', 'Some bold text.')))
    print t
    print t.render(None) 
    print t.is_terminated()

if __name__ == '__main__':
    main()
