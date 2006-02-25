import locale
import codecs
import utils

class Formatter:
    def __init__(self, entries, encoding = locale.getpreferredencoding()):
        self.entries = entries
        self.encoding = encoding
        self.strings = {}
    def newblock(self):
        self.output('\n\\newblock\n')
    
    def newline(self):
        self.output('\n')

    def write_item(self, entry):
        self.output('\n\n\\bibitem{%s}\n' % entry.key)
        try:
            f = getattr(self, "write_" + entry.type.lower())
        except KeyError:
            pass
        f(entry)

    def output_bibliography(self, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        self.output('\\begin{thebibliography}{%s}' % len(self.entries))
        index = 1
        for entry in self.entries:
            self.write_item(entry)
            index += 1
        self.output('\n\\end{thebibliography}\n')
        self.f.close()
        del self.f
