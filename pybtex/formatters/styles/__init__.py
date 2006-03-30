import locale
import codecs
from pybtex import utils
from pybtex.core import FormattedEntry
from pybtex.formatters.backends import latex

class FormatterBase:
    def format_entries(self, entries):
        l = []
        for entry in entries:
            f = getattr(self, "format_" + entry.type.lower())
            text = f(entry).rich_text()
            l.append(FormattedEntry(entry.key, text, entry.label))
        return l
