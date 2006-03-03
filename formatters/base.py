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
        f = getattr(self, "format_" + entry.type.lower())
        l = f(entry)
        text = utils.add_period("\n\\newblock ".join(l))
        self.output(text)

    def output_bibliography(self, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        maxlen = max([len(e.label) for e in self.entries])
        #FIXME: determine label width proprely
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))
        index = 1
        for entry in self.entries:
            self.write_item(entry)
            index += 1
        self.output('\n\\end{thebibliography}\n')
        self.f.close()
        del self.f
