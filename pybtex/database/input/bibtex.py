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

class BibData:
    def __init__(self):
        self.records = {}
        self.macros = {}

    def addRecord(self, s, loc, toks):
        for i in toks:
            entry = Entry(i[0].lower())
            fields = {}
            for field in i[2]:
                value = field[1][0] % tuple([self.macros[arg] for arg in field[1][1]])
                if field[0] in Entry.valid_roles:
                    for name in value.split(' and '):
                        entry.add_person(Person(name), field[0])
                else:
                    entry.fields[field[0]] = value
            #fields['TYPE'] = i[0]
            self.records[i[1]] = entry

    def addMacro(self, s, loc, toks):
        for i in toks:
            s = i[1][0] % tuple([self.macros[arg] for arg in i[1][1]])
            self.macros[i[0]] = s

    def addMacros(self, macros):
        self.macros.update(macros)

class Parser(ParserBase):
    def __init__(self, encoding=None, filename=None):
        ParserBase.__init__(self, encoding)
        self.data = BibData()
        self.filename = filename

        lparenth = Literal('(').suppress()
        rparenth = Literal(')').suppress()
        lbrace = Literal('{').suppress()
        rbrace = Literal('}').suppress()
        def bibtexGroup(s):
            return (lparenth + s + rparenth) | (lbrace + s + rbrace)

        equal = Literal('=').suppress()
        at = Literal('@').suppress()
        comma = Literal(',').suppress()
        quotedString = Combine('"' + ZeroOrMore(CharsNotIn('\"\n\r')) + '"')
        bracedString = Forward()
        bracedString << Combine('{' + ZeroOrMore(CharsNotIn('{}\n\r') | bracedString) + '}')
        bibTeXString = quotedString | bracedString

        name = Word(alphanums + '!$&*+-./:;<>?[]^_`|').setParseAction(downcaseTokens)
        value = Group(delimitedList(bibTeXString | Word(alphanums).setParseAction(downcaseTokens) | Word(nums), delim='#'))

        #fields
        field = Group(name + equal + value)
        field.setParseAction(self.processField)
        fields = Dict(delimitedList(field))

        #String (aka macro)
        string_body = bibtexGroup(fields)
        string = at + CaselessLiteral('STRING').suppress() + string_body
        string.setParseAction(self.data.addMacro)

        #Record
        record_header = at + Word(alphas).setParseAction(upcaseTokens)
        record_name = Word(printables.replace(',', ''))
        record_body = bibtexGroup(record_name + comma + Group(fields))
        record = Group(record_header + record_body)
        record.setParseAction(self.data.addRecord)

        #Comment
        comment_header = Word(alphas) | (at + CaselessLiteral('COMMENT'))
        comment = Suppress(comment_header + lbrace + ZeroOrMore(CharsNotIn('}')) + rbrace)

        #Raw text
        raw_text = CharsNotIn('@').suppress()

        self.BibTeX_BNF = ZeroOrMore(comment | raw_text | Suppress(string) | Suppress(record)) + StringEnd()

    def set_encoding(self, s):
        self._decode = codecs.getdecoder(s)

    def processField(self, s, loc, toks):
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

    def parse_file(self, filename=None, macros=month_names):
        """parse BibTeX file and return a tree"""
        if filename is None:
            filename = self.filename
        self.data.addMacros(macros)
        f = codecs.open(filename, encoding=self.encoding)
        s = f.read()
        f.close()
        try:
            print self.BibTeX_BNF.parseString(s)
            #print self.data.records
            return self.data.records
        except ParseException, e:
            print "%s: syntax error:" % filename
            print e
            sys.exit(1)
