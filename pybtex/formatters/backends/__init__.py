import locale
import codecs

class BackendBase:
    def __init__(self, encoding = None):
        if encoding is None:
            encoding = locale.getpreferredencoding()
        self.encoding = encoding

    def write_prologue(self, maxlen):
        pass

    def write_epilogue(self):
        pass

    def write_bibliography(self, entries, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        #FIXME: determine label width proprely
        maxlen = max([len(e.label) for e in entries])

        self.write_prologue(maxlen)
        for entry in entries:
            self.write_item(entry)
        self.write_epilogue()

        self.f.close()
