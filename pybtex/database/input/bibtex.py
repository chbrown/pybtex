# Copyright (C) 2006, 2007, 2008  Andrey Golovizin
#
# This file is part of pybtex.
#
# pybtex is free software; you can redistribute it and/or modify
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# pybtex is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pybtex; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""BibTeX parser"""

import codecs, locale
from pyparsing import (
        Word, CaselessLiteral, CharsNotIn,
        nums, alphas, alphanums, printables, delimitedList, downcaseTokens,
        Suppress, Combine, Group, Dict,
        Forward, ZeroOrMore, Optional,
        ParseException,
)
from pybtex.core import Entry, Person
from pybtex.database import BibliographyData
from pybtex.database.input import ParserBase

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

def split_name_list(s):
    """
    Split a list of names, separated by ' and '.

    >>> split_name_list('Johnson and Peterson')
    ['Johnson', 'Peterson']
    >>> split_name_list('Armand and Peterson')
    ['Armand', 'Peterson']
    >>> split_name_list('Armand and anderssen')
    ['Armand', 'anderssen']
    >>> split_name_list('What a Strange{ }and Bizzare Name! and Peterson')
    ['What a Strange{ }and Bizzare Name!', 'Peterson']
    >>> split_name_list('What a Strange and{ }Bizzare Name! and Peterson')
    ['What a Strange and{ }Bizzare Name!', 'Peterson']
    """
    after_space = False
    brace_level = 0
    name_start = 0
    names = []
    for pos, char in enumerate(s):
        if char.isspace():
            after_space = True
        elif char == '{':
            brace_level += 1
            after_space = False
        elif char == '}':
            brace_level -= 1
            after_space = False
        elif (brace_level == 0
                and after_space
                and s[pos:pos + 3].lower() == 'and'
                and s[pos + 3:pos+4].isspace()):
            names.append(s[name_start:pos - 1])
            name_start = pos + 4
        else:
            after_space = False
    names.append(s[name_start:])
    return names


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

        quotedString = Combine(Suppress('"') + ZeroOrMore(CharsNotIn('"')).setParseAction(join_lines) + Suppress('"'))
        bracedString = Forward()
        bracedString << Combine(lbrace + ZeroOrMore(CharsNotIn('{}').setParseAction(join_lines) | bracedString) + rbrace)
        bibTeXString = quotedString | bracedString

        macro_substitution = Word(alphanums).setParseAction(self.substitute_macro)
        name = Word(alphanums + '!$&*+-./:;<>?[]^_`|').setParseAction(downcaseTokens)
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
            entry_body = bibtexGroup(Optional(entry_key + comma, None) + Group(fields))
        else:
            entry_body = bibtexGroup(entry_key + comma + Group(fields))
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
        s = codecs.getreader(self.encoding)(stream).read()

        self.macros = dict(self.default_macros)
        self.data = BibliographyData()
        try:
#            entries = dict(entry[0][0] for entry in self.BibTeX_entry.scanString(s))
            self.BibTeX_entry.searchString(s)
            return self.data
        except ParseException, e:
            print "%s: syntax error:" % getattr(stream, 'name', '<NO FILE>')
            print e
            import sys
            sys.exit(1)
