from pybtex import utils
from pybtex.formatters.backends import BackendBase
import codecs

ndash = '--'

def emph(s): return r"\emph{%s}" % s

def it(s):
    return r"\textit{%s}" %s

def bf(s):
    return r"\textbf{%s}"

def sc(s):
    return r"\textsc{%s}"

class Writer(BackendBase):
    def newblock(self):
        self.output('\n\\newblock\n')
    
    def newline(self):
        self.output('\n')

    def write_item(self, entry):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (entry.label, entry.key))
        self.output(entry.text)

    def write_bibliography(self, entries, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        maxlen = max([len(e.label) for e in entries])
        #FIXME: determine label width proprely
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))
        for entry in entries:
            self.write_item(entry)
        self.output('\n\\end{thebibliography}\n')
        self.f.close()
        del self.f
