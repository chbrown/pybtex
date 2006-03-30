from pybtex import utils
from pybtex.richtext import Tag, Character
from pybtex.formatters.backends import BackendBase
import codecs

ndash = '--'

class Writer(BackendBase):
    symbols = {
        'ndash': '--',
        'newblock': '\n\\newblock '
    }
    
    def format_tag(self, tag_name, text):
        return r'\%s{%s}' % (tag_name, text)
    
    def write_item(self, entry):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (entry.label, entry.key))
        self.output(entry.text.render(self))

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
