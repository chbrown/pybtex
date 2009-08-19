# Copyright (C) 2007, 2008, 2009  Andrey Golovizin
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""BibTeX-like name formatting.

>>> name = 'Charles Louis Xavier Joseph de la Vallee Poussin'
>>> print format(name, '{vv~}{ll}{, jj}{, f.}')
de~la Vallee~Poussin, C.~L. X.~J.
>>> name = 'abc'
>>> print format(name, '{vv~}{ll}{, jj}{, f.}')
abc
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
    def to_python(self):
        return repr(self.text)


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

    def to_python(self):
        from pybtex.style.names import name_part
        class NamePart(object):
            def __init__(self, part, abbr=False):
                self.part = part
                self.abbr = abbr
            def __repr__(self):
                abbr = 'abbr' if self.abbr else ''
                return 'person.%s(%s)' % (self.part, abbr)

        kwargs = {}
        if self.pre_text:
            kwargs['before'] = self.pre_text
        if self.tie:
            kwargs['tie'] = True

        return repr(name_part(**kwargs) [
            NamePart(self.types[self.format_char], self.abbreviate)
        ])
        

class NameFormat(object):
    def __init__(self, format):
        self.format_string = format
        self.parts = name_format_grammar.parseString(format)

    def format(self, name):
        person = Person(name)
        return ''.join(part.format(person) for part in self.parts)

    def to_python(self):
        """Convert BibTeX name format to Python (inexactly)."""
        from pybtex.style.names import join
        parts = ',\n'.join(' ' * 8 + part.to_python() for part in self.parts)
        comment = ' ' * 4 + (
            '"""Format names similarly to %s in BibTeX."""' % self.format_string
        )
        body = ' ' * 4 + 'return join [\n%s,\n]' % parts
        return '\n'.join([
            'def format_names(person, abbr=False):',
            comment,
            body,
        ])


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

    >>> print join(['a', 'long', 'long', 'road'])
    a~long long~road
    >>> print join(['very', 'long', 'phrase'])
    very long~phrase
    """

    if len(words) <= 2:
        return tie.join(words)
    else:
        return (words[0] + tie_or_space(words[0], tie, space) +
                space.join(words[1:-1]) +
                tie + words[-1])

def format(name, format):
    return NameFormat(format).format(name)

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
