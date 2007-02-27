# Copyright 2006 Andrey Golovizin
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
from pyparsing import *
from pybtex.core import Entry, Person
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

class Parser(ParserBase):
    def __init__(self, encoding=None, filename=None, **kwargs):
        ParserBase.__init__(self, encoding)
        self.filename = filename

        lparenth = Literal('(').suppress()
        rparenth = Literal(')').suppress()
        lbrace = Literal('{').suppress()
        rbrace = Literal('}').suppress()
        def bibtexGroup(s):
            return (lparenth + s + rparenth) | (lbrace + s + rbrace)

        at = Suppress('@')
        comma = Suppress(',')
        quotedString = Combine('"' + ZeroOrMore(CharsNotIn('\"\n\r')) + '"')
        bracedString = Forward()
        bracedString << Combine('{' + ZeroOrMore(CharsNotIn('{}\n\r') | bracedString) + '}')
        bibTeXString = quotedString | bracedString

        name = Word(alphanums + '!$&*+-./:;<>?[]^_`|').setParseAction(downcaseTokens)
        value = Group(delimitedList(bibTeXString | Word(alphanums).setParseAction(downcaseTokens) | Word(nums), delim='#'))

        #fields
        field = Group(name + Suppress('=') + value)
        field.setParseAction(self.process_field)
        fields = Dict(delimitedList(field))

        #String (aka macro)
        string_body = bibtexGroup(fields)
        string = at + CaselessLiteral('STRING').suppress() + string_body
        string.setParseAction(self.process_macro)

        #Record
        record_header = at + Word(alphas).setParseAction(downcaseTokens)
        record_key = Word(printables.replace(',', ''))
        if kwargs.get('allow_keyless_entries', False):
            record_body = bibtexGroup(Optional(record_key + comma, None) + Group(fields))
        else:
            record_body = bibtexGroup(record_key + comma + Group(fields))
        record = record_header + record_body
        record.setParseAction(self.process_record)

        self.BibTeX_entry = string | record

    def set_encoding(self, s):
        self._decode = codecs.getdecoder(s)

    def process_field(self, s, loc, toks):
        result = []
        for token in toks:
            strings = []
            args = []
            for s in token[1]:
                s = s.replace('%', '%%')
                if (s.startswith('"') and s.endswith('"')) or \
                   (s.startswith('{') and s.endswith('}')):
                    strings.append(s[1:-1])
                elif s.isdigit():
                    strings.append(str(s))
                else:
                    strings.append('%s')
                    args.append(s)
            result.append((token[0], ("".join(strings), args)))
        return result

    def process_record(self, s, loc, toks):
        entry = Entry(toks[0].lower())
        fields = {}
        key = toks[1]
        if key is None:
            key = 'unnamed-%i' % self.unnamed_entry_counter
            self.unnamed_entry_counter += 1
        for field in toks[2]:
            value = field[1][0] % tuple([self.macros[arg] for arg in field[1][1]])
            if field[0] in Entry.valid_roles:
                for name in value.split(' and '):
                    entry.add_person(Person(name), field[0])
            else:
                entry.fields[field[0]] = value
        return (key, entry)

    def process_macro(self, s, loc, toks):
        for i in toks:
            s = i[1][0] % tuple([self.macros[arg] for arg in i[1][1]])
            self.macros[i[0]] = s

    def parse_file(self, filename=None, macros=month_names):
        """parse BibTeX file and return a tree
        """
        if filename is None:
            filename = self.filename
        self.macros = dict(macros)
        self.unnamed_entry_counter = 1
        f = codecs.open(filename, encoding=self.encoding)
        s = f.read()
        f.close()
        try:
            return dict(entry[0][0] for entry in self.BibTeX_entry.scanString(s))
        except ParseException, e:
            print "%s: syntax error:" % filename
            print e
            sys.exit(1)
