import locale
import codecs
from pybtex.core import FormattedEntry
from pybtex.richtext import Symbol, Phrase
#from pybtex.formatters.backends import latex

class FormatterBase:
    sep = Symbol('newblock')
    def default_phrase(self, *args, **kwargs):
        kwargs['sep'] = self.sep
        kwargs['add_period'] = True
        kwargs['add_periods'] = True
        return Phrase(*args, **kwargs)
    def format_entries(self, entries):
        l = []
        for entry in entries:
            f = getattr(self, "format_" + entry.type.lower())
            text = f(entry).rich_text()
            l.append(FormattedEntry(entry.key, text, entry.label))
        return l
