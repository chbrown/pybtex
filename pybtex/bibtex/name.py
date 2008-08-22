"""BibTeX-like name formatting.

>>> name = 'Charles Louis Xavier Joseph de la Vallee Poussin'
>>> print format(name, '{vv~}{ll}{, jj}{, f.}')
de~la Vallee~Poussin, C.~L. X.~J.
"""

from pyparsing import (
        Literal, Word, Forward, Combine, Group, Suppress, ZeroOrMore,
        Optional, StringEnd, CharsNotIn, alphas, removeQuotes,
)
from pybtex.core import Person
from pybtex.bibtex.utils import bibtex_len

class BibTeXNameFormatError(Exception):
    pass


class Text(object):
    def __init__(self, text):
        self.text = text[0]
    def format(self, person):
        return self.text


class NamePart(object):
    def __init__(self, format_list):
        self.pre_text, format_chars, self.delimiter, self.post_text = format_list[0]

        if self.post_text.endswith('~~'):
            self.tie = '~~'
        elif self.post_text.endswith('~'):
            self.tie = '~'
        else:
            self.tie = None

        self.post_text = self.post_text.rstrip('~')

        l = len(format_chars)
        if l == 1:
            self.abbreviate = True
        elif l == 2 and format_chars[0] == format_chars[1]:
            self.abbreviate = False
        else:
            raise BibTeXNameFormatError('invalid format string')
        self.format_char = format_chars[0]

    types = {
            'f': 'bibtex_first',
            'l': 'last',
            'v': 'prelast',
            'j': 'lineage'
    }

    def format(self, person):
        names = getattr(person, self.types[self.format_char])()

        if not names:
            return ''

        if self.abbreviate:
            names = [name[0] for name in names]
        if self.delimiter is None:
            if self.abbreviate:
                names = join(names, '.~', '. ')
            else:
                names = join(names)
        else:
            names = self.delimiter.join(names)
        formatted_part = self.pre_text + names + self.post_text

        if self.tie == '~':
            discretionary = tie_or_space(formatted_part)
        elif self.tie == '~~':
            discretionary = '~'
        else:
            discretionary = ''

        return formatted_part + discretionary


enough_chars = 3

def tie_or_space(word, tie='~', space = ' '):
    if bibtex_len(word) < enough_chars:
        return tie
    else:
        return space
    

def join(words, tie='~', space=' '):
    """Join some words, inserting ties (~) when nessessary.
    Ties are inserted:
    - after the first word, if it is short
    - before the last word
    Otherwise space is inserted.
    Should produce the same oubput as BibTeX.
    """

    if len(words) <= 2:
        return tie.join(words)
    else:
        return (words[0] + tie_or_space(words[0], tie, space) +
                space.join(words[1:-1]) +
                tie + words[-1])

def format(name, format):
    f = name_format_grammar.parseString(format)
    p = Person(name)
    return ''.join(part.format(p) for part in f)

lbrace = Literal('{')
rbrace = Literal('}')
format_chars = Word(alphas)
braced_string = Forward()
braced_string << Combine(lbrace + ZeroOrMore(CharsNotIn('{}')| braced_string) + rbrace)
verbatim = Combine(ZeroOrMore(CharsNotIn(alphas + '{}') | braced_string))
delimiter = braced_string.copy().setParseAction(removeQuotes)
group = Group(Suppress(lbrace) + verbatim + format_chars + Optional(delimiter, None) +
        verbatim + Suppress(rbrace))
group.setParseAction(NamePart)
toplevel_text = CharsNotIn('{}').setParseAction(Text)
name_format_grammar = ZeroOrMore(toplevel_text | group) + StringEnd()
name_format_grammar.leaveWhitespace()
