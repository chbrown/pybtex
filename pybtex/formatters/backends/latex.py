import re
from pybtex import utils
from pybtex.formatters.backends import BackendBase
import codecs

dash_re = re.compile(r'-')
ndash = '--'

class Backend(BackendBase):
    def newblock(self):
        self.output('\n\\newblock\n')
    
    def newline(self):
        self.output('\n')

    def write_item(self, entry):
        self.output('\n\n\\bibitem{%s}\n' % entry[0])
        self.output(entry[1])

    def output_bibliography(self, entries, filename):
        self.f = codecs.open(filename, "w", self.encoding)
        self.output = self.f.write
        maxlen = max([len(e[2]) for e in entries])
        #FIXME: determine label width proprely
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))
        for entry in entries:
            self.write_item(entry)
        self.output('\n\\end{thebibliography}\n')
        self.f.close()
        del self.f

    def emph(self, s):
        return r"\emph{%s}" % s

    def it(self, s):
        return r"\textit{%s}" %s

    def bf(self, s):
        return r"\textbf{%s}"

    def sc(self, s):
        return r"\textsc{%s}"

    def dashify(self, s):
        return ndash.join(dash_re.split(s))
