import locale
import codecs
from pybtex import utils
from pybtex.formatters.backends import latex

class FormatterBase:
    def __init__(self, entries, encoding = locale.getpreferredencoding()):
        self.separator = '\n\\newblock\n'
        self.word_separator = ', '
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
        text = f(entry)
        self.output(unicode(text))

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
