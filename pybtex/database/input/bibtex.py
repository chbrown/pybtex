# Copyright (C) 2006, 2007, 2008, 2009  Andrey Golovizin
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

"""BibTeX parser"""

from pyparsing import (
        Word, Literal, CaselessLiteral, CharsNotIn,
        nums, alphas, alphanums, printables, delimitedList, downcaseTokens,
        Suppress, Combine, Group, Dict,
        Forward, ZeroOrMore, Optional,
        ParseException,
)
import pybtex.io
from pybtex.core import Entry, Person
from pybtex.database.input import ParserBase
from pybtex.bibtex.utils import split_name_list

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

file_extension = 'bib'

def join_lines(s, loc, toks):
    return [' '.join(tok.splitlines()) for tok in toks]

class Parser(ParserBase):
    def __init__(self, encoding=None, macros=month_names, person_fields=Person.valid_roles, **kwargs):
        ParserBase.__init__(self, encoding)

        self.default_macros = dict(macros)
        self.person_fields = person_fields

        lbrace = Suppress('{')
        rbrace = Suppress('}')
        def bibtexGroup(s):
            return ((lbrace + s + rbrace) |
                    (Suppress('(') + s + Suppress(')')))

        at = Suppress('@')
        comma = Suppress(',')

        innerBracedString = Forward()
        innerBracedString << Combine(Literal('{') + ZeroOrMore(CharsNotIn('{}').setParseAction(join_lines) | innerBracedString) + Literal('}'))
        quotedString = Combine(Suppress('"') + ZeroOrMore(CharsNotIn('"{').setParseAction(join_lines) | innerBracedString) + Suppress('"'))
        bracedString = Combine(lbrace + ZeroOrMore(CharsNotIn('{}').setParseAction(join_lines) | innerBracedString) + rbrace)
        bibTeXString = quotedString | bracedString

        name_chars = alphanums + '!$&*+-./:;<>?[\\]^_`|~\x7f'
        macro_substitution = Word(name_chars).setParseAction(self.substitute_macro)
        name = Word(name_chars).setParseAction(downcaseTokens)
        value = Combine(delimitedList(bibTeXString | Word(nums) | macro_substitution, delim='#'), adjacent=False)

        #fields
        field = Group(name + Suppress('=') + value)
        fields = Dict(delimitedList(field))

        #String (aka macro)
        string_body = bibtexGroup(fields)
        string = at + CaselessLiteral('STRING').suppress() + string_body
        string.setParseAction(self.process_macro)

        #preamble
        preamble_body = bibtexGroup(value)
        preamble = at + CaselessLiteral('PREAMBLE').suppress() + preamble_body
        preamble.setParseAction(self.process_preamble)

        #bibliography entry
        entry_header = at + Word(alphas).setParseAction(downcaseTokens)
        entry_key = Word(printables.replace(',', ''))
        if kwargs.get('allow_keyless_entries', False):
            entry_body = bibtexGroup(Optional(entry_key + comma, None) + Group(fields) + Optional(comma))
        else:
            entry_body = bibtexGroup(entry_key + comma + Group(fields) + Optional(comma))
        entry = entry_header + entry_body
        entry.setParseAction(self.process_entry)

        self.BibTeX_entry = string | preamble | entry

    def process_preamble(self, s, loc, toks):
        self.data.add_to_preamble(toks[0])

    def process_entry(self, s, loc, toks):
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

    def substitute_macro(self, s, loc, toks):
        return self.macros[toks[0].lower()]

    def process_macro(self, s, loc, toks):
        self.macros[toks[0][0].lower()] = toks[0][1]

    def parse_stream(self, stream):
        self.unnamed_entry_counter = 1
        s = pybtex.io.reader(stream, self.encoding).read()

        self.macros = dict(self.default_macros)
        try:
#            entries = dict(entry[0][0] for entry in self.BibTeX_entry.scanString(s))
            self.BibTeX_entry.searchString(s)
        except ParseException, e:
            print "%s: syntax error:" % getattr(stream, 'name', '<NO FILE>')
            print e
            import sys
            sys.exit(1)
