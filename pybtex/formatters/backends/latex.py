from pybtex import utils
from pybtex.richtext import Tag
from pybtex.formatters.backends import BackendBase

class Writer(BackendBase):
    symbols = {
        'ndash': '--',
        'newblock': '\n\\newblock '
    }
    
    def format_tag(self, tag_name, text):
        return r'\%s{%s}' % (tag_name, text)
    
    def write_prologue(self, maxlen):
        self.output('\\begin{thebibliography}{%s}' % ('8' * maxlen))

    def write_epilogue(self):
        self.output('\n\\end{thebibliography}\n')

    def write_item(self, entry):
        self.output('\n\n\\bibitem[%s]{%s}\n' % (entry.label, entry.key))
        self.output(entry.text.render(self))
