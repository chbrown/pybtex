# Copyright (c) 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
# 
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
from pybtex.bibtex.utils import bibtex_len, bibtex_first_letter

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
            names = [bibtex_first_letter(name) for name in names]
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
group.setParseAction(lambda toks: NamePart(toks))
toplevel_text = CharsNotIn('{}').setParseAction(lambda toks: Text(toks))
name_format_grammar = ZeroOrMore(toplevel_text | group) + StringEnd()
name_format_grammar.leaveWhitespace()
