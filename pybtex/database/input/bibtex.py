# Copyright (c) 2006, 2007, 2008, 2009, 2010, 2011  Andrey Golovizin
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

"""BibTeX parser

>>> from io import StringIO
>>> parser = Parser()
>>> bib_data = parser.parse_stream(StringIO(u'''
... @String{SCI = "Science"}
... 
... @String{JFernandez = "Fernandez, Julio M."}
... @String{HGaub = "Gaub, Hermann E."}
... @String{MGautel = "Gautel, Mathias"}
... @String{FOesterhelt = "Oesterhelt, Filipp"}
... @String{MRief = "Rief, Matthias"}
... 
... @Article{rief97b,
...   author =       MRief #" and "# MGautel #" and "# FOesterhelt
...                  #" and "# JFernandez #" and "# HGaub,
...   title =        "Reversible Unfolding of Individual Titin
...                  Immunoglobulin Domains by {AFM}",
...   journal =      SCI,
...   volume =       276,
...   number =       5315,
...   pages =        "1109--1112",
...   year =         1997,
...   doi =          "10.1126/science.276.5315.1109",
...   URL =          "http://www.sciencemag.org/cgi/content/abstract/276/5315/1109",
...   eprint =       "http://www.sciencemag.org/cgi/reprint/276/5315/1109.pdf",
... }
... '''))
>>> rief97b = parser.data.entries['rief97b']
>>> authors = rief97b.persons['author']
>>> for author in authors:
...     print unicode(author)
Rief, Matthias
Gautel, Mathias
Oesterhelt, Filipp
Fernandez, Julio M.
Gaub, Hermann E.

"""

from pyparsing import (
        Word, Literal, CaselessLiteral, CharsNotIn,
        nums, alphas, alphanums, printables, delimitedList, downcaseTokens,
        Suppress, Combine, Group, Dict,
        Forward, ZeroOrMore, Optional,
        ParseException,
)
import pybtex.io
from pybtex.core import Entry, Person
from pybtex.database.input import BaseParser
from pybtex.bibtex.utils import split_name_list
from pybtex.exceptions import PybtexError
from pybtex import textutils

month_names = {
    'jan': 'January',
    'feb': 'February',
    'mar': 'March',
    'apr': 'April',
    'may': 'May',
    'jun': 'June',
    'jul': 'July',
    'aug': 'August',
    'sep': 'September',
    'oct': 'October',
    'nov': 'November',
    'dec': 'December'
}


def normalize_whitespace(s, loc, toks):
    return [textutils.normalize_whitespace(tok) for tok in toks]


class Parser(BaseParser):
    name = 'bibtex'
    suffixes = '.bib',
    unicode_io = True

    def __init__(self, encoding=None, macros=month_names, person_fields=Person.valid_roles, **kwargs):
        BaseParser.__init__(self, encoding)

        self.macros = dict(macros)
        self.person_fields = person_fields

        lbrace = Suppress('{')
        rbrace = Suppress('}')
        def bibtexGroup(s):
            return ((lbrace + s + rbrace) |
                    (Suppress('(') + s + Suppress(')')))

        at = Suppress('@')
        comma = Suppress(',')

        innerBracedString = Forward()
        innerBracedString << Combine(Literal('{') + ZeroOrMore(CharsNotIn('{}') | innerBracedString) + Literal('}'))
        quotedString = Combine(Suppress('"') + ZeroOrMore(CharsNotIn('"{') | innerBracedString) + Suppress('"'))
        bracedString = Combine(lbrace + ZeroOrMore(CharsNotIn('{}') | innerBracedString) + rbrace)
        bibTeXString = (quotedString | bracedString)

        name_chars = alphanums + '!$&*+-./:;<>?[\\]^_`|~\x7f'
        macro_substitution = Word(name_chars).setParseAction(lambda toks: self.substitute_macro(toks))
        name = Word(name_chars).setParseAction(downcaseTokens)
        value = Combine(delimitedList(bibTeXString | Word(nums) | macro_substitution, delim='#'), adjacent=False)
        value.setParseAction(normalize_whitespace)

        #fields
        field = Group(name + Suppress('=') + value)
        fields = Dict(delimitedList(field))

        #String (aka macro)
        string_body = bibtexGroup(fields)
        string = at + CaselessLiteral('STRING').suppress() + string_body
        string.setParseAction(lambda toks: self.process_macro(toks))

        #preamble
        preamble_body = bibtexGroup(value)
        preamble = at + CaselessLiteral('PREAMBLE').suppress() + preamble_body
        preamble.setParseAction(lambda toks: self.process_preamble(toks))

        #bibliography entry
        entry_header = at + Word(alphas).setParseAction(downcaseTokens)
        entry_key = Word(printables.replace(',', ''))
        if kwargs.get('allow_keyless_entries', False):
            entry_body = bibtexGroup(Optional(entry_key + comma, None) + Group(fields) + Optional(comma))
        else:
            entry_body = bibtexGroup(entry_key + comma + Group(fields) + Optional(comma))
        entry = entry_header + entry_body
        entry.setParseAction(lambda toks: self.process_entry(toks))

        self.BibTeX_entry = string | preamble | entry

    def process_preamble(self, toks):
        self.data.add_to_preamble(toks[0])

    def process_entry(self, toks):
        entry = Entry(toks[0].lower())
        fields = {}
        key = toks[1]

        if key is None:
            key = 'unnamed-%i' % self.unnamed_entry_counter
            self.unnamed_entry_counter += 1

        for k, v in toks[2]:
            if k in self.person_fields:
                for name in split_name_list(v):
                    entry.add_person(Person(name), k)
            else:
                entry.fields[k] = v
#        return (key, entry)
        self.data.add_entry(key, entry)

    def substitute_macro(self, toks):
        key = toks[0].lower()
        try:
            return self.macros[key]
        except KeyError:
            raise PybtexError('undefined macro %s' % key)

    def process_macro(self, toks):
        self.macros[toks[0][0].lower()] = toks[0][1]

    def parse_stream(self, stream):
        self.unnamed_entry_counter = 1

        try:
#            entries = dict(entry[0][0] for entry in self.BibTeX_entry.scanString(s))
            self.BibTeX_entry.searchString(stream.read())
        except ParseException, e:
            print "%s: syntax error:" % getattr(stream, 'name', '<NO FILE>')
            print e
            import sys
            sys.exit(1)
        return self.data
