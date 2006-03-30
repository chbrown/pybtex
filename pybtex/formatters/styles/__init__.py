import locale
import codecs
from pybtex import utils
from pybtex.core import FormattedEntry
from pybtex.richtext import Symbol
#from pybtex.formatters.backends import latex

class FormatterBase:
    sep = Symbol('newblock')
    def default_phrase(self):
        return utils.Phrase(sep=self.sep, sep2=self.sep, add_period=True, add_periods=True)
    def format_entries(self, entries):
        l = []
        for entry in entries:
            f = getattr(self, "format_" + entry.type.lower())
            text = f(entry).rich_text()
            l.append(FormattedEntry(entry.key, text, entry.label))
        return l
